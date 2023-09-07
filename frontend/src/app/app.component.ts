import { Component, isDevMode, OnDestroy, OnInit } from '@angular/core';
import {
  BehaviorSubject,
  combineLatest,
  exhaustMap,
  filter,
  map,
  shareReplay,
  startWith,
  Subject,
  switchMap,
  takeUntil,
  timer,
} from 'rxjs';
import { Book, BookService } from './book.service';
import { environment } from '../environments/environment';
import { SwUpdate } from '@angular/service-worker';
import { fromPromise } from 'rxjs/internal/observable/innerFrom';

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
  protected page$ = new BehaviorSubject(0);
  protected bookResponse$ = combineLatest([this.query$, this.page$]).pipe(
    switchMap(([query, page]) =>
      this.bookService.list(query, page).pipe(startWith(undefined)),
    ),
    shareReplay(1),
  );
  protected books$ = this.bookResponse$.pipe(map((r) => r?.items));
  protected totalBookCount$ = this.bookResponse$.pipe(
    filter((r) => !!r),
    map((r) => r?.total_item_count),
  );
  protected selectedTab = 0;

  constructor(
    private readonly bookService: BookService,
    private readonly swUpdate: SwUpdate,
  ) {}

  ngOnInit() {
    this.websocket = new WebSocket(`${environment.wsApiBase}/book/purchases`);
    this.websocket.onmessage = (message) =>
      (this.purchases = [JSON.parse(message.data), ...this.purchases]);

    if (isDevMode()) return;

    timer(0, 5 * 60_000)
      .pipe(
        exhaustMap(() => fromPromise(this.swUpdate.checkForUpdate())),
        takeUntil(this.destroy$),
      )
      .subscribe();

    this.swUpdate.versionUpdates
      .pipe(
        filter((e) => e.type === 'VERSION_READY'),
        takeUntil(this.destroy$),
      )
      .subscribe(
        () =>
          confirm(
            'A new version of this app is available. Do you want to reload?',
          ) && location.reload(),
      );
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
