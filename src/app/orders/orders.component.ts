import { Component, OnInit } from '@angular/core';
import { CartService } from '../cart.service';
import { HttpClient } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit {
  cartItems: any[] = [];

  constructor(private cartService: CartService, private http: HttpClient, private toastr: ToastrService, private router: Router) {}

  ngOnInit(): void {
    this.cartItems = this.cartService.getCartItems();
  }

  removeFromCart(index: number): void {
    this.cartService.removeItem(index);
    this.cartItems = this.cartService.getCartItems(); // Refresh the cart items
  }

  calculateLinePrice(item: any): number {
    return item.price * item.quantity;
  }

  calculateSubtotal(): number {
    return this.cartItems.reduce((acc, item) => acc + this.calculateLinePrice(item), 0);
  }

  calculateShipping(): string {
    return 'Free';
  }

  calculateTotalPriceWithShipping(): number {
    return this.calculateSubtotal();
  }

  checkout(): void {
    const orderItems = this.cartItems.map(item => ({
      menuItemId: item.id,
      quantity: item.quantity
      // name:item.name,
      // price: item.price,
      // description: item.description,
      // imageUrl: item.imageUrl
    }));

    this.http.post('http://localhost:8083/api/orders/checkout', orderItems)
      .subscribe(
        (response) => {
          this.toastr.success('Order placed successfully!', 'Success');
          this.cartService.clearCart();
          this.router.navigate(['/home']);
        },
        (error) => {
          this.toastr.error('Failed to place order.', 'Error');
        }
      );
  }
}
