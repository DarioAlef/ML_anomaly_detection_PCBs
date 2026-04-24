import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface AnalyzeResponse {
  original_b64:  string;
  heatmap_b64:   string;
  anomaly_score: number;
  verdict:       string;
  inference_ms:  number;
}

@Injectable({ providedIn: 'root' })
export class InspectionService {
  private readonly base = environment.apiUrl;

  constructor(
    private http: HttpClient,
  ) {}

  /**
   * Envia imagem para análise de anomalia e retorna original + heatmap em base64.
   * Endpoint síncrono — retorna quando o processamento termina.
   */
  analyzeImage(file: File): Observable<AnalyzeResponse> {
    const form = new FormData();
    form.append('file', file, file.name);

    return this.http.post<AnalyzeResponse>(
      `${this.base}/inspection/analyze`,
      form,
    );
  }
}
