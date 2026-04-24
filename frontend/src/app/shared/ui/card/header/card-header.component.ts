import { Component, input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'div[appCardHeader]',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './card-header.component.html',
  styleUrl: './card-header.component.scss',
  host: {
    '[class]': 'className()',
  },
})
export class CardHeaderComponent {
  className = input<string>('');
}