import { Component, input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'div[appCardFooter]',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './card-footer.component.html',
  styleUrl: './card-footer.component.scss',
  host: {
    '[class]': 'className()',
  },
})
export class CardFooterComponent {
  className = input<string>('');
}