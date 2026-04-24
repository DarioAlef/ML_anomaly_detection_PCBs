import { Component, input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export type BadgeVariant = 'default' | 'secondary' | 'outline' | 'destructive';

@Component({
    selector: 'div[appBadge], span[appBadge]',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './badge.component.html',
    styleUrl: './badge.component.scss'
})
export class BadgeComponent {
    variant = input<BadgeVariant>('default');
    className = input<string>('');
}
