import os, textwrap
def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    open(path, 'w').write(content)
    print(f'Written: {path}')
w('tailwind.config.js', '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,ts}'],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#01696f', light: '#00838a', dark: '#004f54' },
        shift: { scheduled:'#FFC107', confirmed:'#4CAF50', alert:'#EF5350', pending:'#FF9800', open:'#90CAF9', cancelled:'#BDBDBD' },
        surface: { page:'#F5F5F5', card:'#FFFFFF', header:'#FAFAFA', today:'#E3F2FD' },
        border: { DEFAULT:'#E0E0E0', strong:'#BDBDBD' },
        text: { primary:'#212121', secondary:'#757575', inverse:'#FFFFFF' }
      },
      fontFamily: { sans: ['Inter','Roboto','sans-serif'] },
      fontSize: { xs:'11px', sm:'12px', base:'13px', md:'14px', lg:'16px', xl:'18px', '2xl':'20px' },
      spacing: { 0:'0', 1:'4px', 2:'8px', 3:'12px', 4:'16px', 5:'20px', 6:'24px', 8:'32px', 10:'40px', 12:'48px' },
      borderRadius: { sm:'4px', DEFAULT:'6px', md:'8px', lg:'12px', full:'9999px' },
      boxShadow: { card:'0 1px 3px rgba(0,0,0,0.12)', hover:'0 4px 8px rgba(0,0,0,0.15)' }
    }
  },
  plugins: []
}
''')
w('src/styles.scss', ''':root {
  --color-primary: #01696f; --color-primary-light: #00838a; --color-primary-dark: #004f54;
  --color-shift-scheduled: #FFC107; --color-shift-confirmed: #4CAF50;
  --color-shift-alert: #EF5350; --color-shift-pending: #FF9800;
  --color-shift-open: #90CAF9; --color-shift-cancelled: #BDBDBD;
  --surface-page: #F5F5F5; --surface-card: #FFFFFF; --surface-header: #FAFAFA;
  --surface-today: #E3F2FD; --border-color: #E0E0E0;
  --text-primary: #212121; --text-secondary: #757575;
  --font-family: 'Inter', 'Roboto', sans-serif;
  --radius-sm: 4px; --radius: 6px; --radius-md: 8px;
  --shadow-card: 0 1px 3px rgba(0,0,0,0.12);
}
@tailwind base; @tailwind components; @tailwind utilities;
* { box-sizing: border-box; }
body { font-family: var(--font-family); background: var(--surface-page); color: var(--text-primary); margin: 0; }
.mat-mdc-button { font-family: var(--font-family) !important; }
''')
w('src/app/core/models/shift.model.ts', '''export type ShiftStatus = 'scheduled'|'confirmed'|'alert'|'pending'|'open'|'cancelled';
export interface Shift { id:string; clientId:string; clientName:string; caregiverId:string; caregiverName:string; serviceType:string; date:Date; startTime:string; endTime:string; timezone:string; status:ShiftStatus; isRecurring:boolean; statusCodes:string[]; }
export interface CalendarClient { id:string; name:string; office:string; clientType:string; shifts:Shift[]; }
export interface CalendarFilter { search:string; office:string; clientType:string; supervisor:string; viewMode:'week'|'day'; dateRange:{start:Date; end:Date}; showDetails:boolean; }
export const STATUS_COLOR_MAP:Record<ShiftStatus,string> = { scheduled:'#FFC107', confirmed:'#4CAF50', alert:'#EF5350', pending:'#FF9800', open:'#90CAF9', cancelled:'#BDBDBD' };
export const STATUS_LABEL_MAP:Record<ShiftStatus,string> = { scheduled:'Schd', confirmed:'Confirmed', alert:'Alert', pending:'Pending', open:'Open', cancelled:'Cancelled' };
''')
w('src/app/core/services/scheduling.service.ts', '''import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";
import { CalendarClient, CalendarFilter, Shift, ShiftStatus } from "../models/shift.model";
@Injectable({ providedIn: "root" })
export class SchedulingService {
  private today = new Date(2025,6,20);
  private clients$ = new BehaviorSubject<CalendarClient[]>(this.getMockClients());
  getClients(): Observable<CalendarClient[]> { return this.clients$.asObservable(); }
  getWeekDates(start: Date): Date[] {
    return Array.from({length:7},(_,i)=>{ const d=new Date(start); d.setDate(start.getDate()+i); return d; });
  }
  isToday(date: Date): boolean { const t=new Date(); return date.toDateString()===t.toDateString(); }
  private makeShift(id:string,clientId:string,clientName:string,date:Date,start:string,end:string,service:string,caregiver:string,status:ShiftStatus): Shift {
    return {id,clientId,clientName,caregiverId:'c1',caregiverName:caregiver,serviceType:service,date,startTime:start,endTime:end,timezone:'EST',status,isRecurring:true,statusCodes:[]};
  }
  private getMockClients(): CalendarClient[] {
    const d = (offset:number)=>{ const dt=new Date(this.today); dt.setDate(dt.getDate()+offset); return dt; };
    const clients = [
      {id:'cl1',name:'William, John',office:'Main',clientType:'Standard'},
      {id:'cl2',name:'Smith, Mary',office:'Main',clientType:'Premium'},
      {id:'cl3',name:'Johnson, Robert',office:'Branch',clientType:'Standard'},
      {id:'cl4',name:'Davis, Linda',office:'Main',clientType:'Premium'},
      {id:'cl5',name:'Martinez, Carlos',office:'Branch',clientType:'Standard'},
      {id:'cl6',name:'Brown, Patricia',office:'Main',clientType:'Standard'},
      {id:'cl7',name:'Wilson, Jennifer',office:'Branch',clientType:'Premium'},
      {id:'cl8',name:'Moore, Michael',office:'Main',clientType:'Standard'},
      {id:'cl9',name:'Taylor, Barbara',office:'Branch',clientType:'Premium'},
      {id:'cl10',name:'Anderson, Thomas',office:'Main',clientType:'Standard'}
    ];
    const statuses:ShiftStatus[]=['scheduled','confirmed','alert','pending','open','cancelled','scheduled','confirmed'];
    const services=['Companion Care','Special Home Services','New Respite Care','Personal Care'];
    const caregivers=['Wilson, Bob','Johnson, Ann','Davis, Tom','Smith, Mary'];
    return clients.map((c,ci)=>({...c, shifts: Array.from({length:7},(_,di)=>[
      di%3!==1 ? this.makeShift(`s-${c.id}-${di}`,c.id,c.name,d(di-3),'10:30a','11:30a',services[ci%4],caregivers[ci%4],statuses[ci%8]) : null,
      di%2===0 ? this.makeShift(`s2-${c.id}-${di}`,c.id,c.name,d(di-3),'4:15a','5:30a',services[(ci+2)%4],caregivers[(ci+1)%4],statuses[(ci+2)%8]) : null
    ].filter(Boolean) as Shift[]).flat()}));
  }
}
''')
p='src/app/features/scheduling/components'
w(f'{p}/filter-toolbar/filter-toolbar.component.ts', '''import{Component,EventEmitter,Output,OnInit}from"@angular/core";
import{FormBuilder,FormGroup}from"@angular/forms";
import{CalendarFilter}from"../../../../core/models/shift.model";
@Component({selector:"app-filter-toolbar",templateUrl:"./filter-toolbar.component.html",styleUrls:["./filter-toolbar.component.scss"]})
export class FilterToolbarComponent implements OnInit{
  @Output() filterChanged=new EventEmitter<CalendarFilter>();
  @Output() viewModeChanged=new EventEmitter<string>();
  form!:FormGroup;
  offices=['All Offices','Main','Branch'];
  clientTypes=['All Types','Standard','Premium'];
  supervisors=['All Supervisors','supervisor_filter'];
  viewModes=['Week','Day','Month'];
  currentWeekLabel='7/17 - 7/23';
  constructor(private fb:FormBuilder){}
  ngOnInit(){this.form=this.fb.group({search:'',office:'All Offices',clientType:'All Types',supervisor:'All Supervisors',viewMode:'Week',showDetails:false});}
  apply(){this.filterChanged.emit(this.form.value);}
  reset(){this.form.reset({search:'',office:'All Offices',clientType:'All Types',supervisor:'All Supervisors',viewMode:'Week',showDetails:false}); this.apply();}
  prevWeek(){} nextWeek(){} goToday(){}
}
''')
w(f'{p}/filter-toolbar/filter-toolbar.component.html','''<div class="filter-toolbar flex flex-wrap items-center gap-2 px-4 py-2 bg-surface-header border-b border-border">
  <form [formGroup]="form" class="flex flex-wrap items-center gap-2 flex-1">
    <mat-form-field appearance="outline" class="filter-field">
      <mat-icon matPrefix>search</mat-icon>
      <input matInput formControlName="search" placeholder="Search">
    </mat-form-field>
    <mat-form-field appearance="outline" class="filter-field">
      <mat-select formControlName="office"><mat-option *ngFor="let o of offices" [value]="o">{{o}}</mat-option></mat-select>
    </mat-form-field>
    <mat-form-field appearance="outline" class="filter-field">
      <mat-select formControlName="clientType"><mat-option *ngFor="let c of clientTypes" [value]="c">{{c}}</mat-option></mat-select>
    </mat-form-field>
    <mat-form-field appearance="outline" class="filter-field">
      <mat-select formControlName="supervisor"><mat-option *ngFor="let s of supervisors" [value]="s">{{s}}</mat-option></mat-select>
    </mat-form-field>
    <button mat-flat-button color="primary" (click)="apply()" class="apply-btn">Apply</button>
    <button mat-button (click)="reset()" class="text-text-secondary">Reset</button>
  </form>
  <div class="flex items-center gap-2 ml-auto">
    <mat-slide-toggle formControlName="showDetails" class="text-sm">Show Details</mat-slide-toggle>
    <mat-form-field appearance="outline" class="filter-field w-24">
      <mat-select formControlName="viewMode"><mat-option *ngFor="let v of viewModes" [value]="v">{{v}}</mat-option></mat-select>
    </mat-form-field>
    <div class="flex items-center gap-1">
      <button mat-icon-button (click)="prevWeek()"><mat-icon>chevron_left</mat-icon></button>
      <span class="text-sm font-medium text-text-primary px-2">{{currentWeekLabel}}</span>
      <button mat-icon-button (click)="nextWeek()"><mat-icon>chevron_right</mat-icon></button>
    </div>
    <button mat-stroked-button (click)="goToday()" class="today-btn">Today</button>
  </div>
</div>''')
w(f'{p}/filter-toolbar/filter-toolbar.component.scss','''.filter-toolbar{background:var(--surface-header);border-bottom:1px solid var(--border-color);min-height:48px;} .filter-field{height:36px;font-size:13px;} .filter-field .mat-mdc-form-field-subscript-wrapper{display:none;} .apply-btn{background:var(--color-primary)!important;color:#fff;font-size:13px;height:36px;} .today-btn{border-color:var(--color-primary)!important;color:var(--color-primary)!important;}''')
w(f'{p}/shift-card/shift-card.component.ts','''import{Component,Input}from"@angular/core";
import{Shift,STATUS_COLOR_MAP}from"../../../../core/models/shift.model";
@Component({selector:"app-shift-card",templateUrl:"./shift-card.component.html",styleUrls:["./shift-card.component.scss"]})
export class ShiftCardComponent{@Input() shift!:Shift; @Input() compact=false;
  get bgColor(){return STATUS_COLOR_MAP[this.shift.status];}
  get timeLabel(){return `${this.shift.startTime}-${this.shift.endTime} ${this.shift.timezone}`;}
}''')
w(f'{p}/shift-card/shift-card.component.html','''<div class="shift-card" [style.background-color]="bgColor" [class.compact]="compact">
  <div class="flex items-start justify-between">
    <div class="flex-1 min-w-0">
      <div class="shift-time"><strong>{{shift.startTime}}-{{shift.endTime}}</strong> {{shift.timezone}}</div>
      <div class="shift-service truncate">{{shift.serviceType}}</div>
      <div class="shift-caregiver truncate">{{shift.caregiverName}}</div>
    </div>
    <div class="flex flex-col items-end gap-1">
      <mat-checkbox class="shift-check"></mat-checkbox>
      <mat-icon *ngIf="shift.isRecurring" class="shift-recurring text-xs">repeat</mat-icon>
    </div>
  </div>
</div>''')
w(f'{p}/shift-card/shift-card.component.scss','''.shift-card{border-radius:4px;padding:4px 6px;font-size:11px;cursor:pointer;transition:box-shadow 0.15s;min-height:52px;margin-bottom:2px;border-left:3px solid rgba(0,0,0,0.15);} .shift-card:hover{box-shadow:0 2px 6px rgba(0,0,0,0.2);} .shift-time{font-size:11px;font-weight:600;color:#212121;white-space:nowrap;} .shift-service{font-size:11px;color:#424242;margin-top:1px;} .shift-caregiver{font-size:10px;color:#616161;} .shift-check{transform:scale(0.7);} .shift-recurring{font-size:12px!important;color:#616161;}''')
w(f'{p}/scheduling-calendar/scheduling-calendar.component.ts','''import{Component,OnInit,OnDestroy}from"@angular/core";
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
''')
w(f'{p}/scheduling-calendar/scheduling-calendar.component.html','''<div class="scheduling-page flex flex-col h-screen bg-surface-page">
  <!-- PAGE HEADER -->
  <div class="page-header flex items-center justify-between px-6 py-3 bg-white border-b border-border">
    <div class="flex items-center gap-3">
      <mat-icon class="text-primary">calendar_today</mat-icon>
      <h1 class="text-xl font-semibold text-text-primary">Scheduling</h1>
      <span class="text-sm text-text-secondary">Home / Scheduling / Schedule Calendar</span>
    </div>
    <div class="flex items-center gap-2">
      <button mat-flat-button color="primary" class="publish-btn">Publish</button>
      <button mat-icon-button color="warn"><mat-icon>delete</mat-icon></button>
      <button mat-icon-button class="text-yellow-500"><mat-icon>warning</mat-icon></button>
      <button mat-icon-button color="primary"><mat-icon>add_circle</mat-icon></button>
    </div>
  </div>
  <!-- FILTER TOOLBAR -->
  <app-filter-toolbar (filterChanged)="onFilterChanged($event)"></app-filter-toolbar>
  <!-- CALENDAR GRID -->
  <div class="calendar-wrap flex-1 overflow-auto">
    <table class="calendar-table w-full border-collapse">
      <thead>
        <tr>
          <th class="client-col bg-surface-header border-b border-r border-border text-left px-4 py-2 text-sm font-semibold text-text-secondary sticky left-0 z-10">Client</th>
          <th *ngFor="let date of weekDates" class="day-col border-b border-r border-border text-center px-2 py-2" [class.today-col]="isToday(date)" [style.background]="isToday(date)?'var(--surface-today)':'var(--surface-header)'">
            <div class="text-xs font-medium text-text-secondary uppercase">{{dayNames[date.getDay()]}}</div>
            <div class="text-lg font-bold" [class.text-primary]="isToday(date)">{{date.getMonth()+1}}/{{date.getDate()}}</div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let client of pagedClients" class="calendar-row hover:bg-gray-50 transition-colors">
          <td class="client-col bg-white border-b border-r border-border px-4 py-2 sticky left-0 z-10 min-w-44">
            <div class="font-medium text-sm text-text-primary">{{client.name}}</div>
            <div class="text-xs text-text-secondary">{{client.office}} | {{client.clientType}}</div>
          </td>
          <td *ngFor="let date of weekDates" class="day-cell border-b border-r border-border p-1 align-top" [class.today-cell]="isToday(date)" [style.background]="isToday(date)?'rgba(227,242,253,0.3)':'transparent'">
            <app-shift-card *ngFor="let shift of getShiftsForDay(client,date)" [shift]="shift"></app-shift-card>
            <div *ngIf="getShiftsForDay(client,date).length===0" class="empty-cell h-12"></div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <!-- STATUS BAR -->
  <div class="status-bar flex items-center justify-between px-4 py-2 bg-white border-t border-border">
    <div class="flex items-center gap-1 text-sm text-text-secondary">
      <button mat-icon-button [disabled]="currentPage===1" (click)="currentPage=1"><mat-icon>first_page</mat-icon></button>
      <button mat-icon-button [disabled]="currentPage===1" (click)="currentPage=currentPage-1"><mat-icon>chevron_left</mat-icon></button>
      <span>Showing {{(currentPage-1)*pageSize+1}}-{{min(currentPage*pageSize,totalItems)}} of {{totalItems}}</span>
      <button mat-icon-button [disabled]="currentPage===totalPages" (click)="currentPage=currentPage+1"><mat-icon>chevron_right</mat-icon></button>
      <button mat-icon-button [disabled]="currentPage===totalPages" (click)="currentPage=totalPages"><mat-icon>last_page</mat-icon></button>
    </div>
    <div class="flex items-center gap-2 flex-wrap">
      <span *ngFor="let s of statusLegend" class="legend-chip" [style.background]="s.color+20" [style.border-color]="s.color">{{s.key}}</span>
    </div>
  </div>
</div>''')
w(f'{p}/scheduling-calendar/scheduling-calendar.component.scss','''.scheduling-page{font-family:var(--font-family);} .page-header{background:#fff;min-height:56px;} .publish-btn{background:var(--color-primary)!important;} .calendar-table{table-layout:fixed;} .client-col{width:180px;min-width:180px;background:var(--surface-header);} .day-col{width:calc((100%-180px)/7);min-width:120px;} .today-col{background:var(--surface-today)!important;} .today-cell{background:rgba(227,242,253,0.3);} .calendar-row:nth-child(even) .client-col{background:#fafafa;} .legend-chip{display:inline-flex;align-items:center;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600;border:1.5px solid;margin:0 2px;} .status-bar{min-height:40px;border-top:1px solid var(--border-color);}''')
w('src/app/app.module.ts','''import{NgModule}from"@angular/core";
import{BrowserModule}from"@angular/platform-browser";
import{BrowserAnimationsModule}from"@angular/platform-browser/animations";
import{ReactiveFormsModule}from"@angular/forms";
import{MatToolbarModule}from"@angular/material/toolbar";
import{MatButtonModule}from"@angular/material/button";
import{MatIconModule}from"@angular/material/icon";
import{MatFormFieldModule}from"@angular/material/form-field";
import{MatInputModule}from"@angular/material/input";
import{MatSelectModule}from"@angular/material/select";
import{MatCheckboxModule}from"@angular/material/checkbox";
import{MatSlideToggleModule}from"@angular/material/slide-toggle";
import{MatPaginatorModule}from"@angular/material/paginator";
import{MatTooltipModule}from"@angular/material/tooltip";
import{MatChipsModule}from"@angular/material/chips";
import{AppRoutingModule}from"./app-routing.module";
import{AppComponent}from"./app.component";
import{FilterToolbarComponent}from"./features/scheduling/components/filter-toolbar/filter-toolbar.component";
import{ShiftCardComponent}from"./features/scheduling/components/shift-card/shift-card.component";
import{SchedulingCalendarComponent}from"./features/scheduling/components/scheduling-calendar/scheduling-calendar.component";
@NgModule({declarations:[AppComponent,FilterToolbarComponent,ShiftCardComponent,SchedulingCalendarComponent],
imports:[BrowserModule,BrowserAnimationsModule,ReactiveFormsModule,AppRoutingModule,
MatToolbarModule,MatButtonModule,MatIconModule,MatFormFieldModule,MatInputModule,MatSelectModule,MatCheckboxModule,MatSlideToggleModule,MatPaginatorModule,MatTooltipModule,MatChipsModule],
bootstrap:[AppComponent]})
export class AppModule{}
''')
w('src/app/app.component.ts','''import{Component}from"@angular/core";@Component({selector:"app-root",template:"<app-scheduling-calendar></app-scheduling-calendar>"})export class AppComponent{}''')
w('src/app/app.component.html','<app-scheduling-calendar></app-scheduling-calendar>')
w('src/app/app.component.scss',''':host{display:block;height:100vh;}''')
min=lambda a,b:a if a<b else b
print('All files written successfully!')
