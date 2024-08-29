import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../auth.service';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  signUpForm: FormGroup;
  signInForm: FormGroup;
  signUpError!: string;
  signInError!: string;

  constructor(private fb: FormBuilder, private authService: AuthService, private toast: ToastrService,private  router: Router) {
    this.signUpForm = this.fb.group({
      username: ['', Validators.required],
      lastname: [' ', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      address: ['', Validators.required],
      phone: ['', Validators.required],
      password: ['', Validators.required],

    });

    this.signInForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', Validators.required]
    });
  }

  ngOnInit(): void {}

  onSignUpSubmit(): void {
    console.log('SignUp form submitted');
    if (this.signUpForm.valid) {
      this.authService.signUp(this.signUpForm.value).subscribe(
        (response) => {
          if (response.message) {
            this.toast.success(response.message);
            this.router.navigate(['/login']);
          } else {
            this.signUpError = 'Unexpected response from server';
            this.toast.error(this.signUpError);
          }
        },
        (error) => {
          this.signUpError = error.error.error || 'An unexpected error occurred.';
          this.toast.error(this.signUpError);
        }
      );
    } else {
      console.log('Form is invalid');
      this.signUpError = 'Please fill in all required fields.';
      this.toast.warning(this.signUpError);
    }
  }








  signUp(): void {
    const container = document.getElementById('container');
    if (container) {
      container.classList.add('right-panel-active');
    }
  }

  signIn(): void {
    const container = document.getElementById('container');
    if (container) {
      container.classList.remove('right-panel-active');
    }
  }
  preventNavigation(event: Event): void {
    event.preventDefault();
  }

  onSignInSubmit(): void {
    if (this.signInForm.valid) {
      this.authService.signIn(this.signInForm.value.username, this.signInForm.value.password).subscribe(
        (response) => {
          localStorage.setItem('token', response.token);
          this.toast.success('Login successful!');
          this.router.navigate(['/profile']);
        },
        (error) => {
          this.signInError = 'Invalid username or password.';
          this.toast.error('Invalid username or password!');
        }
      );
    }
  }


}
