import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  Validators,
  AbstractControl,
  ValidationErrors,
} from '@angular/forms';
import { CalendarFilter } from '../../../../core/models/shift.model';

/**
 * FilterToolbarComponent
 * 
 * 4-Layer Architecture:
 * Layer 1 - PRESENTATION: Search input and primary filters (office, client type, supervisor)
 * Layer 2 - CONTAINER: View configuration (show details toggle, view mode selector)
 * Layer 3 - FEATURE: Week navigation controls
 * Layer 4 - CORE: Today button (primary action)
 * 
 * Security: Implements OWASP best practices for input validation and XSS prevention
 * Accessibility: WCAG 2.1 Level AA compliance with aria-labels and live regions
 */
@Component({
  selector: 'app-filter-toolbar',
  templateUrl: './filter-toolbar.component.html',
  styleUrls: ['./filter-toolbar.component.scss'],
})
export class FilterToolbarComponent implements OnInit {
  @Output() filterChanged = new EventEmitter<CalendarFilter>();
  @Output() viewModeChanged = new EventEmitter<string>();

  form!: FormGroup;

  // Layer 1: Presentation Data
  offices = ['All Offices', 'Main', 'Branch'];
  clientTypes = ['All Types', 'Standard', 'Premium'];
  supervisors = ['All Supervisors', 'supervisor_filter'];

  // Layer 2: Container Data
  viewModes = ['Week', 'Day', 'Month'];

  // Layer 3 & 4: Feature & Core Data
  currentWeekLabel = '7/17 - 7/23';

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.initializeForm();
    this.setupFormValueChanges();
  }

  /**
   * Initialize the reactive form with validators
   * Implements OWASP input validation and XSS prevention
   */
  private initializeForm(): void {
    this.form = this.fb.group({
      search: [
        '',
        [
          Validators.maxLength(100),
          this.sanitizeSearchValidator.bind(this),
        ],
      ],
      office: ['All Offices', Validators.required],
      clientType: ['All Types', Validators.required],
      supervisor: ['All Supervisors', Validators.required],
      viewMode: ['Week', Validators.required],
      showDetails: [false],
    });
  }

  /**
   * Custom validator for XSS detection (OWASP A03:2021 - Injection)
   * Detects common XSS attack patterns
   */
  private sanitizeSearchValidator(
    control: AbstractControl
  ): ValidationErrors | null {
    if (!control.value) {
      return null;
    }

    const value = control.value.toString();

    // XSS pattern detection
    const xssPatterns = [
      /<script[\s\S]*?<\/script>/gi, // Script tags
      /javascript:/gi, // JavaScript protocol
      /on\w+\s*=/gi, // Event handlers (onclick, onload, etc.)
      /<iframe[\s\S]*?<\/iframe>/gi, // iFrame tags
      /<img[\s\S]*?on\w+/gi, // Image with event handlers
      /&lt;script|&lt;iframe/gi, // Encoded script/iframe tags
      /&#[\d]{2,};/gi, // Numeric entities
    ];

    for (const pattern of xssPatterns) {
      if (pattern.test(value)) {
        return { xssDetected: true };
      }
    }

    // Control character detection
    if (/[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]/g.test(value)) {
      return { xssDetected: true };
    }

    return null;
  }

  /**
   * Sanitize search input by removing/encoding dangerous characters (OWASP)
   */
  private sanitizeSearchInput(input: string): string {
    if (!input) {
      return '';
    }

    // Remove control characters
    let sanitized = input.replace(/[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]/g, '');

    // HTML entity encoding
    const entityMap: { [key: string]: string } = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
      '/': '&#x2F;',
    };

    sanitized = sanitized.replace(/[&<>"'\/]/g, (char) => entityMap[char]);

    // Trim whitespace
    return sanitized.trim();
  }

  /**
   * Validate filter combination logic
   * Can be extended for complex business rules
   */
  private validateFilterCombination(): boolean {
    // Example: Validate that supervisor is only selected when office is specific
    const office = this.form.get('office')?.value;
    const supervisor = this.form.get('supervisor')?.value;

    if (office === 'All Offices' && supervisor !== 'All Supervisors') {
      console.warn(
        'Warning: Supervisor filter with All Offices may not work as expected'
      );
    }

    return true;
  }

  /**
   * Get accessibility label for filter status (for screen readers)
   */
  getFilterStatusAriaLabel(): string {
    const office = this.form.get('office')?.value ?? 'All Offices';
    const clientType = this.form.get('clientType')?.value ?? 'All Types';
    const supervisor =
      this.form.get('supervisor')?.value ?? 'All Supervisors';
    const showDetails = this.form.get('showDetails')?.value
      ? 'showing details'
      : 'hiding details';

    return `Filters: ${office}, ${clientType}, ${supervisor}. ${showDetails}.`;
  }

  /**
   * Get accessibility label for view mode selector
   */
  getViewModeAriaLabel(): string {
    const currentMode = this.form.get('viewMode')?.value ?? 'Week';
    return `Select calendar view mode. Currently viewing ${currentMode} view.`;
  }

  /**
   * Apply filters (Layer 1 - Presentation action)
   * Emits sanitized filter data to parent component
   */
  apply(): void {
    if (this.form.invalid) {
      console.error('Form validation failed');
      return;
    }

    if (!this.validateFilterCombination()) {
      return;
    }

    // Sanitize search input
    const sanitizedSearch = this.sanitizeSearchInput(
      this.form.get('search')?.value
    );

    // Create filter object with sanitized data
    const filters: CalendarFilter = {
      search: sanitizedSearch,
      office: this.form.get('office')?.value,
      clientType: this.form.get('clientType')?.value,
      supervisor: this.form.get('supervisor')?.value,
      showDetails: this.form.get('showDetails')?.value,
      viewMode: this.form.get('viewMode')?.value,
    };

    this.filterChanged.emit(filters);
  }

  /**
   * Reset all filters to default state (Layer 1 & 2)
   */
  reset(): void {
    this.form.reset(
      {
        search: '',
        office: 'All Offices',
        clientType: 'All Types',
        supervisor: 'All Supervisors',
        viewMode: 'Week',
        showDetails: false,
      },
      { emitEvent: true }
    );

    // Emit reset action
    this.apply();
  }

  /**
   * Navigate to previous week (Layer 3 - Feature)
   * Can be enhanced with date calculations
   */
  prevWeek(): void {
    console.log('Navigate to previous week');
    // TODO: Implement week navigation logic
    // Update currentWeekLabel with previous week dates
    // Emit event to parent component
  }

  /**
   * Navigate to next week (Layer 3 - Feature)
   * Can be enhanced with date calculations
   */
  nextWeek(): void {
    console.log('Navigate to next week');
    // TODO: Implement week navigation logic
    // Update currentWeekLabel with next week dates
    // Emit event to parent component
  }

  /**
   * Navigate to today (Layer 4 - Core / Primary Action)
   * This is the main call-to-action button
   */
  goToday(): void {
    console.log('Navigate to today');
    // TODO: Implement today navigation logic
    // Update currentWeekLabel to current week
    // Emit event to parent component
    // Reset any custom date selections
  }

  /**
   * Setup real-time form value change listeners
   * Useful for dynamic updates or analytics
   */
  private setupFormValueChanges(): void {
    this.form.get('viewMode')?.valueChanges.subscribe((mode: string) => {
      this.viewModeChanged.emit(mode);
    });

    // Monitor search input for real-time validation feedback
    this.form.get('search')?.statusChanges.subscribe((status) => {
      if (status === 'INVALID') {
        // Show validation warning if needed
        console.warn('Search input validation failed');
      }
    });
  }
}
