import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject, of, throwError } from 'rxjs';
import { Router } from '@angular/router';
import { tap, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://localhost:8083/api'; // Your Spring Boot base URL

  private isLoggedInSubject = new BehaviorSubject<boolean>(this.isLoggedIn());

  constructor(private http: HttpClient, private router: Router) {}

  get isLoggedIn$() {
    return this.isLoggedInSubject.asObservable();
  }

  signUp(user: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/register`, user, {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    }).pipe(
      tap(() => {
        console.log('User registered successfully');
      }),
      catchError((error) => {
        console.error('Registration failed', error);
        return of(null);
      })
    );
  }

  getOrdersForCurrentUser(): Observable<any[]> {
    const token = localStorage.getItem('token');
    return this.http.get<any[]>(`${this.apiUrl}/orders/user`, {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${token}`
      })
    }).pipe(
      catchError((error: any) => {
        console.error('Error fetching orders:', error);
        return throwError(error); // rethrow the error after logging it
      })
    );
  }




  signIn(username: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/login`, { username, password }, {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    }).pipe(
      tap((response: any) => {
        if (response && response.token) {
          localStorage.setItem('token', response.token);
          this.isLoggedInSubject.next(true);
        }
      }),
      catchError((error) => {
        console.error('Login failed', error);
        return of(null);
      })
    );
  }


  signOut(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('currentUser');
    this.isLoggedInSubject.next(false);
    this.router.navigate(['/login']);
  }

  getCurrentUser(): Observable<any> {
    const token = localStorage.getItem('token');
    if (token) {
      return this.http.get(`${this.apiUrl}/auth/me`, {
        headers: new HttpHeaders({
          'Authorization': `Bearer ${token}`
        })
      }).pipe(
        catchError((error) => {
          console.error('Fetching current user failed', error);
          return of(null);
        })
      );
    }
    return of(null);
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('token');
  }

  updateUser(user: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/auth/update`, user, {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      })
    }).pipe(
      tap((response: any) => {
        // Check if a new token is returned and update it in localStorage
        if (response && response.token) {
          localStorage.setItem('token', response.token);
          this.isLoggedInSubject.next(true);
        }
      }),
      catchError((error) => {
        console.error('Updating user failed', error);
        return of(null);
      })
    );
  }

}
