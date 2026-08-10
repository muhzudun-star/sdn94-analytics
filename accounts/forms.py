from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class LoginTerpaduForm(AuthenticationForm):
    """Form login tunggal untuk Admin maupun Pengguna (Guru/Wali Kelas).

    Role ditentukan otomatis dari data Profile milik user setelah login berhasil,
    sehingga admin dan user login di satu tempat yang sama.
    """
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Masukkan username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Kata Sandi',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Masukkan kata sandi',
        })
    )

    error_messages = {
        'invalid_login': 'Username atau kata sandi salah. Silakan coba lagi.',
        'inactive': 'Akun ini sudah tidak aktif.',
    }


class RegisterUserForm(UserCreationForm):
    """Form pendaftaran akun baru untuk role Pengguna (Guru/Wali Kelas).

    Pendaftaran mandiri (self-register) hanya diperbolehkan untuk role USER.
    Role ADMIN tetap harus dibuat lewat seeder / Django admin agar tidak
    sembarang orang bisa mendapatkan akses penuh.
    """
    first_name = forms.CharField(
        label='Nama Lengkap',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Masukkan nama lengkap',
            'autofocus': True,
        })
    )
    jabatan = forms.CharField(
        label='Jabatan',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'mis. Wali Kelas 3A (opsional)',
        })
    )
    no_hp = forms.CharField(
        label='No. HP',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'mis. 08xxxxxxxxxx (opsional)',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Buat username',
        })
        self.fields['username'].help_text = None
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Buat kata sandi',
        })
        self.fields['password1'].help_text = None
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Ulangi kata sandi',
        })
        self.fields['password2'].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        # Self-registration selalu mendapat role USER (Guru/Wali Kelas),
        # bukan ADMIN, demi keamanan.
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
            Profile.objects.filter(user=user).update(
                role=Profile.ROLE_USER,
                jabatan=self.cleaned_data.get('jabatan', ''),
                no_hp=self.cleaned_data.get('no_hp', ''),
            )
        return user
