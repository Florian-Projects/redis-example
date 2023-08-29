import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { HttpClient } from '@angular/common/http';
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

  protected readonly dataSource = this.bookService.list();

  constructor(private readonly bookService: BookService) {}

  ngOnInit() {
    // this.bookService
    //   .list()
    //   .pipe(takeUntil(this.destroy$))
    //   .subscribe((books) => console.log({ books }));
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
