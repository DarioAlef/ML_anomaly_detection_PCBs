import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LucideAngularModule, Shield, Scan } from 'lucide-angular';

@Component({
  selector: 'app-hero-section',
  standalone: true,
  imports: [CommonModule, LucideAngularModule],
  styleUrl: './hero-section.component.scss',
  templateUrl: './hero-section.component.html'
})
export class HeroSectionComponent {
  protected readonly ShieldIcon = Shield;
  protected readonly ScanIcon = Scan;
}
