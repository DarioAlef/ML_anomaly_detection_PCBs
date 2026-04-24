import { Component, signal, output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { LucideAngularModule, Home, Info, ChevronRight, ChevronLeft, Cpu } from 'lucide-angular';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, LucideAngularModule, RouterModule],
  styleUrl: './sidebar.component.scss',
  templateUrl: './sidebar.component.html'
})
export class SidebarComponent {
  protected readonly collapsed = signal(false);
  readonly collapsedChange = output<boolean>();

  protected readonly CpuIcon = Cpu;
  protected readonly ChevronRightIcon = ChevronRight;
  protected readonly ChevronLeftIcon = ChevronLeft;

  protected readonly navItems = [
    { icon: Home, label: 'Início', route: '/dashboard' },
    { icon: Info, label: 'Sobre o Projeto', route: '/about' },
  ];

  protected toggle() {
    this.collapsed.update(v => !v);
    this.collapsedChange.emit(this.collapsed());
  }
}
