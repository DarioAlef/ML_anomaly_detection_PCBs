import {
  Component, signal, OnDestroy, HostListener, ElementRef, ViewChild
} from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  LucideAngularModule,
  Brain, Loader2, Upload, Crosshair,
  BarChart3, AlertTriangle, User, RefreshCw, ImageIcon
} from 'lucide-angular';
import { Subscription } from 'rxjs';
import { InspectionService, AnalyzeResponse } from '../../../../core/services/inspection.service';

type State = 'idle' | 'dragging' | 'processing' | 'done' | 'error';

const ACCEPT = ['image/jpeg', 'image/png', 'image/webp', 'image/bmp'];
const MAX_MB = 10;

@Component({
  selector: 'app-inspection-showcase',
  standalone: true,
  imports: [CommonModule, LucideAngularModule],
  styleUrl: './inspection-showcase.component.scss',
  templateUrl: './inspection-showcase.component.html'
})
export class InspectionShowcaseComponent implements OnDestroy {
  // Icons
  protected readonly BrainIcon = Brain;
  protected readonly LoaderIcon = Loader2;
  protected readonly UploadIcon = Upload;
  protected readonly CrosshairIcon = Crosshair;
  protected readonly BarChartIcon = BarChart3;
  protected readonly AlertIcon = AlertTriangle;
  protected readonly UserIcon = User;
  protected readonly ResetIcon = RefreshCw;
  protected readonly ImageIcon = ImageIcon;

  protected readonly MAX_MB = MAX_MB;

  // State
  protected readonly state = signal<State>('idle');
  protected readonly previewSrc = signal<string>('');
  protected readonly result = signal<AnalyzeResponse | null>(null);
  protected readonly errorMsg = signal<string | null>(null);

  private sub?: Subscription;
  private dragCounter = 0; // evita flicker no dragleave

  constructor(private inspectionService: InspectionService) { }

  // ── Drag & Drop ─────────────────────────────────────────────────────────────

  onDragEnter(e: DragEvent): void {
    e.preventDefault();
    this.dragCounter++;
    this.state.set('dragging');
  }

  onDragOver(e: DragEvent): void {
    e.preventDefault();
    e.dataTransfer!.dropEffect = 'copy';
  }

  onDragLeave(e: DragEvent): void {
    e.preventDefault();
    this.dragCounter--;
    if (this.dragCounter <= 0) {
      this.dragCounter = 0;
      this.state.set('idle');
    }
  }

  onDrop(e: DragEvent): void {
    e.preventDefault();
    this.dragCounter = 0;
    const file = e.dataTransfer?.files?.[0];
    if (file) this.processFile(file);
  }

  // ── File input ──────────────────────────────────────────────────────────────

  onFileInputChange(e: Event): void {
    const input = e.target as HTMLInputElement;
    const file = input.files?.[0];
    if (file) this.processFile(file);
    input.value = '';   // reset para permitir re-seleção do mesmo arquivo
  }

  // ── Core ────────────────────────────────────────────────────────────────────

  private processFile(file: File): void {
    // Validação de tipo
    if (!ACCEPT.includes(file.type)) {
      this.errorMsg.set(`Tipo inválido: ${file.type}. Use PNG, JPEG ou WebP.`);
      this.state.set('error');
      return;
    }

    // Validação de tamanho
    if (file.size > MAX_MB * 1024 * 1024) {
      this.errorMsg.set(`Arquivo muito grande (máx. ${MAX_MB} MB).`);
      this.state.set('error');
      return;
    }

    // Preview local imediato
    const reader = new FileReader();
    reader.onload = (ev) => this.previewSrc.set(ev.target!.result as string);
    reader.readAsDataURL(file);

    this.state.set('processing');
    this.result.set(null);
    this.errorMsg.set(null);

    // Envia o arquivo original sem compressão para evitar distorções
    this.sub?.unsubscribe();
    this.sub = this.inspectionService.analyzeImage(file).subscribe({
      next: (res) => {
        this.result.set(res);
        this.state.set('done');
      },
      error: (err: Error) => {
        this.errorMsg.set(err.message ?? 'Erro na inspeção.');
        this.state.set('error');
      },
    });
  }

  /**
   * Redimensiona e comprime a imagem via Canvas antes do upload.
   * Garante que o arquivo fique abaixo do limite do proxy (≈ 1 MB).
   */
  private compressImage(file: File, maxPx = 1024, quality = 0.85): Promise<File> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      const url = URL.createObjectURL(file);

      img.onload = () => {
        URL.revokeObjectURL(url);

        let { width, height } = img;
        if (width > maxPx || height > maxPx) {
          if (width >= height) {
            height = Math.round((height * maxPx) / width);
            width = maxPx;
          } else {
            width = Math.round((width * maxPx) / height);
            height = maxPx;
          }
        }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        canvas.getContext('2d')!.drawImage(img, 0, 0, width, height);

        canvas.toBlob(
          (blob) => {
            if (!blob) { reject(new Error('Falha na compressão.')); return; }
            resolve(new File([blob], file.name.replace(/\.[^.]+$/, '.jpg'), { type: 'image/jpeg' }));
          },
          'image/jpeg',
          quality,
        );
      };

      img.onerror = () => { URL.revokeObjectURL(url); reject(new Error('Imagem inválida.')); };
      img.src = url;
    });
  }

  protected reset(): void {
    this.sub?.unsubscribe();
    this.state.set('idle');
    this.result.set(null);
    this.previewSrc.set('');
    this.errorMsg.set(null);
    this.dragCounter = 0;
  }

  ngOnDestroy(): void {
    this.sub?.unsubscribe();
  }
}
