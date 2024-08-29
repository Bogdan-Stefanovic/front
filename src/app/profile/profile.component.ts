import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  currentUser: any;
  cartItems: any[] = [];
  totalAmountSpent: number = 0;
  totalItemsPurchased: number = 0;
  averageSpendingPerOrder: number = 0;
  favoriteProducts: { name: string, count: number, imageUrl: string }[] = [];

  previousTotalAmountSpent: number = 0;
  previousTotalItemsPurchased: number = 0;
  previousAverageSpendingPerOrder: number = 0;

  totalAmountSpentChange: number = 0;
  totalItemsPurchasedChange: number = 0;
  averageSpendingPerOrderChange: number = 0;
  orders: any[] = [];

  // Pagination variables
  itemsPerPage: number = 4; // Set items per page to 4
  currentPage: number = 1;
  pagedItems: any[] = [];


  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.authService.getCurrentUser().subscribe(
      (user) => {
        this.currentUser = user;
        if (!this.currentUser.profilePicture) {
          this.currentUser.profilePicture = 'https://example.com/default-profile-picture.png'; // Default profile picture URL
        }
        if (this.currentUser && this.currentUser.orders) {
          this.cartItems = this.currentUser.orders;
          this.loadPreviousPeriodData();
          this.calculateTotalAmountSpent();
          this.calculateTotalItemsPurchased();
          this.calculateAverageSpendingPerOrder();
          this.calculateChanges();
          this.updatePagedItems();
          this.calculateFavoriteProducts();
        }
        this.loadOrders();
      },
      (error) => {
        console.error('Error:', error);
      }
    );
  }





  calculateTotalAmountSpent(): void {
    this.totalAmountSpent = this.orders.reduce((total, order) => {
      return total + order.orderItems.reduce((itemTotal: number, item: { menuItem: { price: number; }; quantity: number; }) => itemTotal + (item.menuItem.price * item.quantity), 0);
    }, 0);
  }

  calculateTotalItemsPurchased(): void {
    this.totalItemsPurchased = this.orders.reduce((total, order) => total + order.orderItems.length, 0);
  }

  calculateAverageSpendingPerOrder(): void {
    const numberOfOrders = this.orders.length;
    this.averageSpendingPerOrder = numberOfOrders > 0 ? this.totalAmountSpent / numberOfOrders : 0;
  }

  calculateChanges(): void {
    console.log('Previous Total Spent:', this.previousTotalAmountSpent);
    console.log('Current Total Spent:', this.totalAmountSpent);
    this.totalAmountSpentChange = this.calculatePercentageChange(this.previousTotalAmountSpent, this.totalAmountSpent);
    console.log('Total Amount Spent Change:', this.totalAmountSpentChange);

    console.log('Previous Items Purchased:', this.previousTotalItemsPurchased);
    console.log('Current Items Purchased:', this.totalItemsPurchased);
    this.totalItemsPurchasedChange = this.calculatePercentageChange(this.previousTotalItemsPurchased, this.totalItemsPurchased);
    console.log('Total Items Purchased Change:', this.totalItemsPurchasedChange);

    console.log('Previous Average Spending:', this.previousAverageSpendingPerOrder);
    console.log('Current Average Spending:', this.averageSpendingPerOrder);
    this.averageSpendingPerOrderChange = this.calculatePercentageChange(this.previousAverageSpendingPerOrder, this.averageSpendingPerOrder);
    console.log('Average Spending Per Order Change:', this.averageSpendingPerOrderChange);

    this.saveCurrentPeriodData();
  }

  loadPreviousPeriodData(): void {
    const previousData = JSON.parse(localStorage.getItem('previousPeriodData') || '{}');
    console.log('Loaded Previous Period Data:', previousData);
    this.previousTotalAmountSpent = previousData.totalAmountSpent || 0;
    this.previousTotalItemsPurchased = previousData.totalItemsPurchased || 0;
    this.previousAverageSpendingPerOrder = previousData.averageSpendingPerOrder || 0;
  }

  saveCurrentPeriodData(): void {
    const currentData = {
      totalAmountSpent: this.totalAmountSpent,
      totalItemsPurchased: this.totalItemsPurchased,
      averageSpendingPerOrder: this.averageSpendingPerOrder
    };
    console.log('Saving Current Period Data:', currentData);
    localStorage.setItem('previousPeriodData', JSON.stringify(currentData));
  }



  calculatePercentageChange(previous: number, current: number): number {
    if (previous === 0) {
      if (current === 0) {
        return 0; // No change if both are zero
      } else {
        return 100; // If the previous is zero and the current is positive, consider it as a 100% increase
      }
    }

    const change = ((current - previous) / previous) * 100;
    return change;
  }


  signOut(): void {
    this.authService.signOut();
  }

  // Pagination methods
  updatePagedItems(): void {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.pagedItems = [];

    // Flatten the order items and distribute them across pages
    this.orders.forEach(order => {
      order.orderItems.forEach((item: any) => {
        this.pagedItems.push({ orderId: order.id, ...item });
      });
    });

    // Slice the pagedItems to show only the items for the current page
    this.pagedItems = this.pagedItems.slice(startIndex, endIndex);

    // Log for debugging
    console.log('Paged Items:', this.pagedItems);
  }

  goToPage(page: number): void {
    if (page < 1 || page > this.totalPages()) {
      return;
    }
    this.currentPage = page;
    this.updatePagedItems();
  }

  totalPages(): number {
    const totalItems = this.orders.reduce((acc, order) => acc + order.orderItems.length, 0);
    return Math.ceil(totalItems / this.itemsPerPage);
  }

  calculateFavoriteProducts(): void {
    const productCounts: { [name: string]: { count: number, imageUrl: string } } = {};

    this.orders.forEach(order => {
      order.orderItems.forEach((item: any) => {
        if (!productCounts[item.menuItem.name]) {
          productCounts[item.menuItem.name] = { count: 0, imageUrl: item.menuItem.image_url };
        }
        productCounts[item.menuItem.name].count += item.quantity;
      });
    });

    this.favoriteProducts = Object.keys(productCounts)
      .map(key => ({
        name: key,
        count: productCounts[key].count,
        imageUrl: productCounts[key].imageUrl
      }))
      .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name)).slice(0, 3); // Sort by count, then by name
  }

  loadOrders(): void {
    this.authService.getOrdersForCurrentUser().subscribe(
      (orders: any) => {
        console.log('Orders:', orders);
        this.orders = orders;

        // Perform calculations
        this.calculateTotalAmountSpent();
        this.calculateTotalItemsPurchased();
        this.calculateAverageSpendingPerOrder();
        this.calculateChanges();
        this.calculateFavoriteProducts();

        // Update pagination
        this.updatePagedItems();
      },
      (error: any) => {
        console.error('Error:', error);
      }
    );
  }
}
