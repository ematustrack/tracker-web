import { Pipe, PipeTransform } from '@angular/core';
import {DomSanitizer} from '@angular/platform-browser';
@Pipe({
  name: 'dataTableDetail'
})
export class DataTableDetailPipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) { }
  transform(value) {
    return this.sanitizer.bypassSecurityTrustUrl(value);
  }
}
