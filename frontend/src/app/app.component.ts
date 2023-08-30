import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { BookService } from './book.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit, OnDestroy {
  private readonly destroy$ = new Subject<void>();

  protected readonly displayedColumns = [
    'id',
    'title',
    'isbn',
    'author',
    'picture',
  ];
  protected readonly purchaseColumns = ['username', 'book_id'];
  protected readonly dataSource = this.bookService.list();
  protected purchases: ReadonlyArray<{ username: string; book_id: string }> =
    [];

  protected websocket?: WebSocket;
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
}
