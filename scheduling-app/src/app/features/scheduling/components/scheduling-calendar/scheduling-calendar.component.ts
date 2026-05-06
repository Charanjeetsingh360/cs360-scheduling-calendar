import{Component,OnInit,OnDestroy}from"@angular/core";
import{SchedulingService}from"../../../../core/services/scheduling.service";
import{CalendarClient,Shift,CalendarFilter}from"../../../../core/models/shift.model";
import{Subject}from"rxjs";import{takeUntil}from"rxjs/operators";
@Component({selector:"app-scheduling-calendar",templateUrl:"./scheduling-calendar.component.html",styleUrls:["./scheduling-calendar.component.scss"]})
export class SchedulingCalendarComponent implements OnInit,OnDestroy{
  private destroy$=new Subject<void>();
  clients:CalendarClient[]=[];
  weekDates:Date[]=[];
  weekStart=new Date(2025,6,17);
  today=new Date();
  currentPage=1; pageSize=10; totalItems=0;
  min = Math.min;
  dayNames=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  statusLegend=[{key:'DS',color:'#FFC107'},{key:'HIS',color:'#FF9800'},{key:'Schd',color:'#2196F3'},{key:'KCBC',color:'#9C27B0'},{key:'Confirmed',color:'#4CAF50'},{key:'NR',color:'#EF5350'},{key:'APPRVD',color:'#009688'},{key:'CONS',color:'#FF5722'}];
  constructor(private svc:SchedulingService){}
  ngOnInit(){this.weekDates=this.svc.getWeekDates(this.weekStart); this.svc.getClients().pipe(takeUntil(this.destroy$)).subscribe(c=>{this.clients=c;this.totalItems=c.length;});}
  ngOnDestroy(){this.destroy$.next();this.destroy$.complete();}
  isToday(d:Date):boolean{return d.toDateString()===this.today.toDateString();}
  getShiftsForDay(client:CalendarClient,date:Date):Shift[]{
    return client.shifts.filter(s=>new Date(s.date).toDateString()===date.toDateString());
  }
  get pagedClients():CalendarClient[]{
    const s=(this.currentPage-1)*this.pageSize; return this.clients.slice(s,s+this.pageSize);
  }
  get totalPages():number{return Math.ceil(this.totalItems/this.pageSize);}
  onFilterChanged(f:CalendarFilter){}
  prevWeek(){this.weekStart=new Date(this.weekStart); this.weekStart.setDate(this.weekStart.getDate()-7); this.weekDates=this.svc.getWeekDates(this.weekStart);}
  nextWeek(){this.weekStart=new Date(this.weekStart); this.weekStart.setDate(this.weekStart.getDate()+7); this.weekDates=this.svc.getWeekDates(this.weekStart);}
}
