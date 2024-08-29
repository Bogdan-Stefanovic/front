import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CartService } from '../cart.service'; // Import CartService
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-menu-item-detail',
  templateUrl: './menu-item-detail.component.html',
  styleUrls: ['./menu-item-detail.component.css']
})
export class MenuItemDetailComponent implements OnInit {
  menuItem: any = {};
  quantity: number = 1;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private cartService: CartService,
    private toastr: ToastrService
  ) {}

  ngOnInit(): void {
    const restaurantId = this.route.snapshot.paramMap.get('restaurantId');
    const menuItemId = this.route.snapshot.paramMap.get('menuItemId');
    this.fetchMenuItemDetails(restaurantId, menuItemId);
  }

  fetchMenuItemDetails(restaurantId: string | null, menuItemId: string | null): void {
    if (restaurantId && menuItemId) {
      this.http.get(`http://localhost:8083/api/restaurants/${restaurantId}/menu-items/${menuItemId}`)
        .subscribe((data: any) => {
          this.menuItem = data;
        });
    }
  }

  incrementQuantity(): void {
    this.quantity++;
  }

  decrementQuantity(): void {
    if (this.quantity > 1) {
      this.quantity--;
    }
  }

  orderNow(): void {
    const existingItem = this.cartService.getCartItems().find(item => item.id === this.menuItem.id);
    if (existingItem) {
      existingItem.quantity += this.quantity;
    } else {
      const itemToAdd = {
        ...this.menuItem,
        quantity: this.quantity
      };
      this.cartService.addToCart(itemToAdd);
    }

    try {
      this.toastr.success('Item added to cart successfully!', 'Success');
    } catch (error) {
      this.toastr.error('Failed to add item to cart.', 'Error');
    }
  }
}
