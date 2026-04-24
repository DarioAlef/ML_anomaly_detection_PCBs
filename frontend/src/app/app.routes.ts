import { Routes } from '@angular/router';
import { DashboardComponent } from './features/dashboard/main/dashboard.component';
import { AboutComponent } from './features/about/about.component';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'about', component: AboutComponent },
  { path: 'challenge', redirectTo: 'dashboard' },
  { path: 'lab', redirectTo: 'dashboard' },
];
