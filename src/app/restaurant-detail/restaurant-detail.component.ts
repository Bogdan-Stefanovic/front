import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../auth.service';
import { CartService } from '../cart.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-restaurant-detail',
  templateUrl: './restaurant-detail.component.html',
  styleUrls: ['./restaurant-detail.component.css']
})
export class RestaurantDetailComponent implements OnInit {
  restaurant: any = {};
  menuItems: any[] = [];
  filteredMenuItems: any[] = [];
  pagedItems: any[] = [];
  currentPage: number = 1;
  itemsPerPage: number = 6;
  totalPages: number = 0;
  totalPagesArray: number[] = [];
  selectedSection: string = 'address';
  hoverSection: string = '';  // Track hover state
  searchQuery: string = '';
  user: any = {};
  profilePicture: string = 'http://bootdey.com/img/Content/avatar/avatar1.png';
  restaurantImageUrl: string = '';
  cheapestItems: any[] = []; // Add this to store the top 3 cheapest items

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private authService: AuthService,
    private router: Router,
    private cartService: CartService,
    private toastr: ToastrService
  ) {}

  ngOnInit(): void {
    this.restaurantImageUrl = history.state.imageUrl;

    this.authService.getCurrentUser().subscribe(
      (user: any) => {
        this.user = user;
        if (this.user && this.user.profilePicture) {
          this.profilePicture = this.user.profilePicture;
        }
      },
      (error: any) => {
        console.error('Error:', error);
      }
    );

    const restaurantId = this.route.snapshot.paramMap.get('id');
    this.fetchRestaurantDetails(restaurantId);
  }

  fetchRestaurantDetails(id: string | null): void {
    if (id) {
      this.http.get(`http://localhost:8083/api/restaurants/${id}`)
        .subscribe((data: any) => {
          this.restaurant = data;
          this.menuItems = data.menuItems;
          this.getCheapestItems(); // Call this method to get the top 3 cheapest items
          this.applyFilters(); // Apply filters initially
        });
    }
  }

  applyFilters(): void {
    let items = this.menuItems;

    // Apply search filter
    if (this.searchQuery) {
      items = items.filter(item =>
        item.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        item.description.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }

    this.filteredMenuItems = items;
    this.updatePagination();
  }

  updatePagination(): void {
    this.totalPages = Math.ceil(this.filteredMenuItems.length / this.itemsPerPage);
    this.totalPagesArray = Array.from({ length: this.totalPages }, (_, i) => i + 1);
    this.updatePagedItems();
  }

  updatePagedItems(): void {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.pagedItems = this.filteredMenuItems.slice(startIndex, endIndex);
  }

  onPageChange(page: number): void {
    if (page < 1 || page > this.totalPages) return;
    this.currentPage = page;
    this.updatePagedItems();
  }

  onSearchChange(): void {
    this.currentPage = 1; // Reset to first page on search
    this.applyFilters();
  }

  selectSection(section: string): void {
    this.selectedSection = section;
  }

  getCheapestItems(): void {
    this.cheapestItems = [...this.menuItems]
      .sort((a, b) => a.price - b.price)
      .slice(0, 3);
  }

  goBack(): void {
    this.router.navigate(['/home']);
    // Navigate back to the previous page
  }

  orderNow(item: any, quantity: number = 1): void {
    const existingItem = this.cartService.getCartItems().find(cartItem => cartItem.id === item.id);
    if (existingItem) {
      existingItem.quantity += quantity; // Increment the quantity if item already exists
      this.cartService.updateCart(existingItem); // Ensure the updated quantity is saved in localStorage
    } else {
      const itemToAdd = {
        ...item,
        quantity: quantity
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
