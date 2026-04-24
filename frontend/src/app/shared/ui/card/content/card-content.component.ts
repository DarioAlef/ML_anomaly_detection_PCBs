import { Component, input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'div[appCardContent]',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './card-content.component.html',
  styleUrl: './card-content.component.scss',
  host: {
    '[class]': 'className()',
  },
})
export class CardContentComponent {
  className = input<string>('');
}