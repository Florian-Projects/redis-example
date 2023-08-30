import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-name-dialog',
  templateUrl: './name-dialog.component.html',
  styleUrls: ['./name-dialog.component.scss'],
})
export class NameDialogComponent {
  constructor(
    protected readonly dialogRef: MatDialogRef<NameDialogComponent>,
  ) {}

  protected onCancel(): void {
    this.dialogRef.close();
  }
}
