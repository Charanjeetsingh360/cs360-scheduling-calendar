import{Component,Input}from"@angular/core";
import{Shift,STATUS_COLOR_MAP}from"../../../../core/models/shift.model";
@Component({selector:"app-shift-card",templateUrl:"./shift-card.component.html",styleUrls:["./shift-card.component.scss"]})
export class ShiftCardComponent{@Input() shift!:Shift; @Input() compact=false;
  get bgColor(){return STATUS_COLOR_MAP[this.shift.status];}
  get timeLabel(){return `${this.shift.startTime}-${this.shift.endTime} ${this.shift.timezone}`;}
}