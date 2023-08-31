import { Component, OnDestroy, OnInit } from '@angular/core';
import { BehaviorSubject, map, startWith, Subject, switchMap } from 'rxjs';
import { Book, BookService } from './book.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit, OnDestroy {
  private readonly destroy$ = new Subject<void>();

  protected purchases: ReadonlyArray<{ username: string; book_id: string }> =
    [];

  protected websocket?: WebSocket;
  protected query$ = new BehaviorSubject('');
  protected books$ = this.query$.pipe(
    switchMap((query) =>
      this.bookService.list(query).pipe(startWith(undefined)),
    ),
    map((response) => response?.items),
  );

  constructor(private readonly bookService: BookService) {}

  ngOnInit() {
    this.websocket = new WebSocket('ws://localhost:8000/book/purchases');
    this.websocket.onmessage = (message) =>
      (this.purchases = [JSON.parse(message.data), ...this.purchases]);
  }

  ngOnDestroy() {
    this.websocket?.close();

    this.destroy$.next();
    this.destroy$.complete();
  }

  protected onPurchase({
    username,
    book,
  }: {
    username: string;
    book: Book;
  }): void {
    this.bookService.purchase(username, book.id).subscribe();
  }
}
