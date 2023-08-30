import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-purchases',
  templateUrl: './purchases.component.html',
  styleUrls: ['./purchases.component.scss'],
})
export class PurchasesComponent {
  @Input() purchases: ReadonlyArray<{
    username: string;
    book_id: string;
  }> = [];

  protected readonly purchaseColumns = ['type', 'username', 'book_id'];
}
