import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { map, Observable, pipe, tap } from 'rxjs';

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
  private static readonly API = 'http://localhost:8000';

  constructor(private readonly http: HttpClient) {}

  list(): Observable<Array<Book>> {
    return this.http
      .get<Array<Book>>(BookService.API + '/books/all')
      .pipe(this.alert_on_error('Failed to fetch book list'));
  }

  get_single(id: number): Observable<Book> {
    return this.http
      .get<Book>(BookService.API + `/books?book_id=${id}`)
      .pipe(this.alert_on_error('Failed to fetch book'));
  }

  private alert_on_error(message: string): any {
    return pipe(
      tap({ error: (e) => alert(`${message}: ${JSON.stringify(e)}`) }),
    );
  }
}
