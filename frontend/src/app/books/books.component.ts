import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Observable } from 'rxjs';
import { Book } from '../book.service';

@Component({
  selector: 'app-books',
  templateUrl: './books.component.html',
  styleUrls: ['./books.component.scss'],
})
export class BooksComponent {
  @Input() books$?: Observable<Array<Book> | undefined>;
  @Input() totalBookCount = 0;
  @Input() hidePagination = false;

  @Output() page = new EventEmitter<number>();
  @Output() purchase = new EventEmitter<Book>();

  protected onBuy(book: Book): void {
    this.purchase.emit(book);
  }
}
