import { Component, input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'div[appCardTitle]',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './card-title.component.html',
  styleUrl: './card-title.component.scss',
  host: {
    '[class]': 'className()',
  },
})
export class CardTitleComponent {
  className = input<string>('');
}