import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private cartItems: any[] = [];
  private cartItemCount = new BehaviorSubject<number>(0);

  constructor() {
    const savedCartItems = localStorage.getItem('cartItems');
    if (savedCartItems) {
      this.cartItems = JSON.parse(savedCartItems);
      this.cartItemCount.next(this.cartItems.length); // Set initial count
    }
  }

  addToCart(item: any): void {
    const existingItem = this.cartItems.find(cartItem => cartItem.id === item.id);
    if (existingItem) {
      existingItem.quantity += item.quantity;
    } else {
      this.cartItems.push(item);
    }
    this.saveCartItems();
    this.cartItemCount.next(this.cartItems.length); // Notify about the count change
  }
  updateCart(updatedItem: any): void {
    const index = this.cartItems.findIndex(item => item.id === updatedItem.id);
    if (index !== -1) {
      this.cartItems[index] = updatedItem; // Update the existing item
      localStorage.setItem('cartItems', JSON.stringify(this.cartItems)); // Save updated cart to localStorage
    }
  }

  getCartItems(): any[] {
    return this.cartItems;
  }

  getCartItemCount() {
    return this.cartItemCount.asObservable(); // Observable for count
  }

  removeItem(index: number): void {
    this.cartItems.splice(index, 1);
    this.saveCartItems();
    this.cartItemCount.next(this.cartItems.length); // Notify about the count change
  }

  clearCart(): void {
    this.cartItems = [];
    this.saveCartItems();
    this.cartItemCount.next(0); // Reset count to zero
  }

  private saveCartItems(): void {
    localStorage.setItem('cartItems', JSON.stringify(this.cartItems));
  }
}
