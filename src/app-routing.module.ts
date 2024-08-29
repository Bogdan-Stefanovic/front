import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {LoginComponent} from "./app/login/login.component";
import {ProfileComponent} from "./app/profile/profile.component";
import {EditComponent} from "./app/edit/edit.component";
import { HomeComponent } from './app/home/home.component';
import { RestaurantDetailComponent } from './app/restaurant-detail/restaurant-detail.component';
import { MenuItemDetailComponent } from './app/menu-item-detail/menu-item-detail.component';import { OrdersComponent } from './app/orders/orders.component';


const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'restaurant/:id', component: RestaurantDetailComponent },
  { path: 'restaurant/:restaurantId/menu-item/:menuItemId', component: MenuItemDetailComponent },
  { path: 'order', component: OrdersComponent }, // Shopping cart route
  { path: '', redirectTo: '/home', pathMatch: 'full' }, // Default route

  { path: 'login', component: LoginComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'edit-profile', component: EditComponent }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
