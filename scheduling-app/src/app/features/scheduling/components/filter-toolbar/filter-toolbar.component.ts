import{Component,EventEmitter,Output,OnInit}from"@angular/core";
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
