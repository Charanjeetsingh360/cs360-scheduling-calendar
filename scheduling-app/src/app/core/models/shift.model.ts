export type ShiftStatus = 'scheduled'|'confirmed'|'alert'|'pending'|'open'|'cancelled';
export interface Shift { id:string; clientId:string; clientName:string; caregiverId:string; caregiverName:string; serviceType:string; date:Date; startTime:string; endTime:string; timezone:string; status:ShiftStatus; isRecurring:boolean; statusCodes:string[]; }
export interface CalendarClient { id:string; name:string; office:string; clientType:string; shifts:Shift[]; }
export interface CalendarFilter { search:string; office:string; clientType:string; supervisor:string; viewMode:'week'|'day'; dateRange:{start:Date; end:Date}; showDetails:boolean; }
export const STATUS_COLOR_MAP:Record<ShiftStatus,string> = { scheduled:'#FFC107', confirmed:'#4CAF50', alert:'#EF5350', pending:'#FF9800', open:'#90CAF9', cancelled:'#BDBDBD' };
export const STATUS_LABEL_MAP:Record<ShiftStatus,string> = { scheduled:'Schd', confirmed:'Confirmed', alert:'Alert', pending:'Pending', open:'Open', cancelled:'Cancelled' };
