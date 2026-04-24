import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http';
import {
  LUCIDE_ICONS, LucideIconProvider,
  Home, Gamepad2, Microscope, Info, Cpu, Activity, Zap,
  Shield, ShieldCheck, Database, Scan, Brain, Loader2, PlayCircle, Crosshair,
  BarChart3, AlertTriangle, User, ChevronRight, ChevronLeft,
} from 'lucide-angular';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideHttpClient(withFetch()),
    {
      provide: LUCIDE_ICONS,
      useValue: new LucideIconProvider({
        home: Home,
        'gamepad-2': Gamepad2,
        microscope: Microscope,
        info: Info,
        cpu: Cpu,
        activity: Activity,
        zap: Zap,
        shield: Shield,
        'shield-check': ShieldCheck,
        database: Database,
        scan: Scan,
        brain: Brain,
        'loader-2': Loader2,
        'play-circle': PlayCircle,
        crosshair: Crosshair,
        'bar-chart-3': BarChart3,
        'alert-triangle': AlertTriangle,
        user: User,
        'chevron-right': ChevronRight,
        'chevron-left': ChevronLeft,
      }),
    },
  ],
};
