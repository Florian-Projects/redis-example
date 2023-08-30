import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, pipe, tap } from 'rxjs';

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
  private static readonly API = 'http://localhost:8000/book';

  constructor(private readonly http: HttpClient) {}

  list(query = ''): Observable<Array<Book>> {
    return this.http
      .get<Array<Book>>(BookService.API + `/search?q=${query}`)
      .pipe(this.alert_on_error('Failed to fetch book list'));
  }

  get_single(id: number): Observable<Book> {
    return this.http
      .get<Book>(BookService.API + `?book_id=${id}`)
      .pipe(this.alert_on_error('Failed to fetch book'));
  }

  private alert_on_error(message: string): any {
    return pipe(
      tap({ error: (e) => alert(`${message}: ${JSON.stringify(e)}`) }),
    );
  }
}
