import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {RouterOutlet} from "@angular/router";
import {AppRoutingModule} from "../app-routing.module";
import {NavbarComponent} from "./navbar/navbar.component";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import { LoginComponent } from './login/login.component';
import { ProfileComponent } from './profile/profile.component';
import {ToastrModule} from "ngx-toastr";
import { FooterComponent } from './footer/footer.component';
import { EditComponent } from './edit/edit.component';
import { AuthInterceptor } from './AuthInterceptor';
import { RestaurantDetailComponent } from './restaurant-detail/restaurant-detail.component';
import { NgxPaginationModule } from 'ngx-pagination';
import { MenuItemDetailComponent } from './menu-item-detail/menu-item-detail.component';
import { OrdersComponent } from './orders/orders.component';
import { CartService } from './cart.service';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    NavbarComponent,
    LoginComponent,
    ProfileComponent,
    FooterComponent,
    EditComponent,
    RestaurantDetailComponent,
    MenuItemDetailComponent,
    OrdersComponent,

  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpClientModule,
    RouterOutlet,
    ReactiveFormsModule,
    BrowserAnimationsModule, // required animations module
    ToastrModule.forRoot(),
    AppRoutingModule,
    NgxPaginationModule

  ],
  providers: [ { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },CartService],
  bootstrap: [AppComponent]
})
export class AppModule { }
