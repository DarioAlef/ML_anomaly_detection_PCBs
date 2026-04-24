import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeroSectionComponent } from '../components/hero-section/hero-section.component';
import { InspectionShowcaseComponent } from '../components/inspection-showcase/inspection-showcase.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    HeroSectionComponent,
    InspectionShowcaseComponent
  ],
  styleUrl: './dashboard.component.scss',
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent { }
