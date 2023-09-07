import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Observable } from 'rxjs';
import { Book } from '../book.service';
import { MatDialog } from '@angular/material/dialog';
import { NameDialogComponent } from '../name-dialog/name-dialog.component';

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
  @Output() purchase = new EventEmitter<{ username: string; book: Book }>();

  constructor(private readonly dialog: MatDialog) {}

  protected onBuy(book: Book): void {
    this.dialog
      .open(NameDialogComponent)
      .afterClosed()
      .subscribe((username) => this.purchase.emit({ username, book }));
  }
}
