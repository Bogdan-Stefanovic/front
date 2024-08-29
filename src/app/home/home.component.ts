import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  restaurants: any[] = [];
  user: any = {};
  profilePicture: string = 'http://bootdey.com/img/Content/avatar/avatar1.png';
  selectedFile: File | null = null;
  cheapestItems: any[] = []; // Store the top 5 cheapest items
  mostExpensiveItems: any[] = []; // Store the most expensive items from each restaurant

  constructor(private http: HttpClient, private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.fetchRestaurants();
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

  fetchRestaurants(): void {
    this.http.get('http://localhost:8083/api/restaurants')
      .subscribe((data: any) => {
        this.restaurants = data.map((restaurant: any, index: number) => {
          const imageUrls = [
            'https://i.pinimg.com/564x/db/4e/d9/db4ed9e296cb978fa441172bfa495a33.jpg',
            'https://i.pinimg.com/564x/58/f3/4d/58f34d9b52b8e08a3815a6bffc2a3773.jpg',
            'https://i.pinimg.com/564x/7a/14/5a/7a145a9458b40af7e0300501663304c4.jpg',
            'https://i.pinimg.com/564x/8c/ed/05/8ced055a36bb35210d1ff208b5028f63.jpg',
            'https://i.pinimg.com/736x/7c/9a/09/7c9a09be8652d13214ac5fa13bd09326.jpg',
            'https://i.pinimg.com/564x/50/9b/8c/509b8c1b340783845d0f745c777429e9.jpg'
          ];
          return {
            ...restaurant,
            imageUrl: imageUrls[index % imageUrls.length]  // Use the image URL based on the index
          };
        });
        this.getMostExpensiveAndCheapestItems(); // Populate the sidebars

      });
  }


  viewProductDetails(item: any): void {
    console.log('Navigating to:', item.restaurantId, item.menuItemId);
    if (item.restaurantId && item.menuItemId) {
      this.router.navigate(['/restaurant', item.restaurantId, 'menu-item', item.menuItemId]);
    } else {
      console.error('Invalid route parameters:', item);
    }
  }




  getMostExpensiveAndCheapestItems(): void {
    this.mostExpensiveItems = this.restaurants.map(restaurant => {
      const maxPriceItem = restaurant.menuItems.reduce((prev: { price: number; }, current: { price: number; }) => (prev.price > current.price) ? prev : current);
      return {
        restaurantId: restaurant.id,
        menuItemId: maxPriceItem.id,
        name: maxPriceItem.name,
        price: maxPriceItem.price,
        imageUrl: maxPriceItem.imageUrl
      };
    });

    this.cheapestItems = this.restaurants.map(restaurant => {
      const minPriceItem = restaurant.menuItems.reduce((prev: { price: number; }, current: { price: number; }) => (prev.price < current.price) ? prev : current);
      return {
        restaurantId: restaurant.id,
        menuItemId: minPriceItem.id,
        name: minPriceItem.name,
        price: minPriceItem.price,
        imageUrl: minPriceItem.imageUrl
      };
    });
  }



  viewRestaurant(id: number, imageUrl: string): void {
    this.router.navigate([`/restaurant/${id}`], { state: { imageUrl } });
  }

  filterFood(category: string): void {
    // Implement filtering logic if you have a category field in your API response.
  }
}

