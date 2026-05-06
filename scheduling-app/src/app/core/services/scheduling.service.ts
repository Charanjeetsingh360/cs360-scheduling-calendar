import { Injectable } from "@angular/core";
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
