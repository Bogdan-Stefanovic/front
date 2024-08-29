import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { ToastrService } from "ngx-toastr";

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css']
})
export class EditComponent implements OnInit {
  user: any = {};
  profilePicture: string = 'http://bootdey.com/img/Content/avatar/avatar1.png';
  selectedFile: File | null = null;

  constructor(private authService: AuthService, private router: Router, private toast: ToastrService) { }

  ngOnInit(): void {
    this.authService.getCurrentUser().subscribe(
      (user) => {
        this.user = user;
        if (this.user && this.user.profilePicture) {
          this.profilePicture = this.user.profilePicture;
        }
      },
      (error) => {
        console.error('Error:', error);
      }
    );
  }


  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file && file.size < 5 * 1024 * 1024) { // less than 5 MB
      this.selectedFile = file;

      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.profilePicture = e.target.result;
        this.user.profilePicture = this.profilePicture; // Set the profile picture in user object
      };
      reader.readAsDataURL(file);
    } else {
      alert('File is too large or not an image.');
    }
  }

  uploadNewImage(): void {
    if (this.selectedFile) {
      const reader = new FileReader();
      reader.onload = () => {
        const base64Image = reader.result as string;
        // this.authService.updateProfilePicture(base64Image);
        this.user.profilePicture = base64Image; // Update local user profile picture
        this.profilePicture = base64Image; // Update the displayed profile picture
        this.toast.success('Profile picture updated successfully');
      };
      reader.readAsDataURL(this.selectedFile);
    }
  }

  saveChanges(): void {
    this.authService.updateUser(this.user).subscribe(
      () => {
        this.toast.success('Profile updated successfully');
        this.router.navigate(['/profile']); // Navigate to profile after update
      },
      (error: any) => {
        this.toast.error('Error updating profile');
      }
    );
  }

}
