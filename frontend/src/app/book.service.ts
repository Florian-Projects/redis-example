import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, pipe, tap } from 'rxjs';
import { environment } from '../environments/environment';

export interface Book {
  id: number;
  title: string;
  isbn: string;
  author: string;
  cover_picture: string;
}

@Injectable({
  providedIn: 'root',
})
export class BookService {
  private static readonly API = `${environment.apiBase}/book`;

  constructor(private readonly http: HttpClient) {}

  list(
    query = '',
    page = 0,
  ): Observable<{ items: Array<Book>; total_item_count: number }> {
    return this.http
      .get<Array<Book>>(BookService.API, {
        params: { query, page_number: page },
      })
      .pipe(this.alert_on_error('Failed to fetch book list'));
  }

  get_single(id: number): Observable<Book> {
    return this.http
      .get<Book>(BookService.API + `/${id}`)
      .pipe(this.alert_on_error('Failed to fetch book'));
  }

  purchase(username: string, bookId: number): Observable<unknown> {
    return this.http.post(BookService.API + `/${bookId}/buy`, {
      username,
    });
  }

  private alert_on_error(message: string): any {
    return pipe(
      tap({ error: (e) => alert(`${message}: ${JSON.stringify(e)}`) }),
    );
  }
}
