import { Component, input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'div[appCardDescription]',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './card-description.component.html',
  styleUrl: './card-description.component.scss',
  host: {
    '[class]': 'className()',
  },
})
export class CardDescriptionComponent {
  className = input<string>('');
}