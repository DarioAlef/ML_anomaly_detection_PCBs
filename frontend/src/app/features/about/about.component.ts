import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LucideAngularModule, Info, Zap, Microscope, Cpu, ShieldCheck, Database } from 'lucide-angular';

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [CommonModule, LucideAngularModule],
  templateUrl: './about.component.html',
  styleUrl: './about.component.scss'
})
export class AboutComponent {
  protected readonly InfoIcon = Info;
  protected readonly ZapIcon = Zap;
  protected readonly MicroscopeIcon = Microscope;
  protected readonly CpuIcon = Cpu;
  protected readonly ShieldIcon = ShieldCheck;
  protected readonly DatabaseIcon = Database;
}
