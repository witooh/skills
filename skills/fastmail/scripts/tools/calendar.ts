import { CalDAVClient } from '../caldav-client.js';
import { DAVCalendar } from 'tsdav';
import { v4 as uuidv4 } from 'uuid';

export interface Calendar {
  id: string;
  name: string;
  description?: string;
  color?: string;
  timezone?: string;
}

// Reminder/Alarm types
export interface Reminder {
  id: string;           // Unique ID for this reminder
  trigger: string;      // Duration before event (e.g., "-PT15M", "-PT1H", "-P1D")
  action: 'display' | 'audio' | 'email';  // Alarm action type
  description?: string; // Reminder description
  minutesBefore?: number; // Parsed minutes for easy access
}

export interface CreateReminderOptions {
  minutesBefore?: number;  // Minutes before event (e.g., 15, 30, 60)
  hoursBefore?: number;    // Hours before event (e.g., 1, 2, 24)
  daysBefore?: number;     // Days before event (e.g., 1, 7)
  action?: 'display' | 'audio' | 'email';  // Default: 'display'
  description?: string;    // Reminder description
}

export interface CalendarEvent {
  id: string;
  calendarId: string;
  title: string;
  description?: string;
  location?: string;
  start: string;      // ISO 8601 in UTC+7
  end: string;        // ISO 8601 in UTC+7
  isAllDay: boolean;
  recurrence?: string;
  attendees?: { name?: string; email: string }[];
  etag?: string;
  url?: string;
  reminders?: Reminder[];  // List of reminders/alarms
}

export interface CreateEventOptions {
  title: string;
  start: string;      // ISO 8601 in UTC+7
  end: string;        // ISO 8601 in UTC+7
  description?: string;
  location?: string;
  allDay?: boolean;
  attendees?: { name?: string; email: string }[];
  reminders?: CreateReminderOptions[];  // Optional reminders to add
}

export interface CreateRecurringEventOptions extends CreateEventOptions {
  recurrence: 'daily' | 'weekly' | 'monthly' | 'yearly';
  recurrenceCount?: number;
  recurrenceUntil?: string;  // YYYY-MM-DD
}

export class CalendarTools {
  constructor(private client: CalDAVClient) {}

  // Convert UTC+7 to UTC for storage
  private toUTC(localDate: string): string {
    // Parse the UTC+7 datetime string properly
    let dateStr = localDate;
    
    // Remove timezone indicator if present
    if (dateStr.includes('+07:00')) {
      dateStr = dateStr.replace('+07:00', '');
    } else if (dateStr.includes('+0700')) {
      dateStr = dateStr.replace('+0700', '');
    }
    
    // Parse as UTC+7 by treating the input as local time in Bangkok
    // Then convert to UTC by subtracting 7 hours
    const [datePart, timePart] = dateStr.split('T');
    const [year, month, day] = datePart.split('-').map(Number);
    const [hour, minute, second] = (timePart || '00:00:00').split(':').map(Number);
    
    // Create date in UTC+7
    const utc7Date = new Date(Date.UTC(year, month - 1, day, hour, minute, second || 0));
    // Subtract 7 hours to get UTC
    const utcDate = new Date(utc7Date.getTime() - (7 * 60 * 60 * 1000));
    
    return utcDate.toISOString();
  }

  // Format date to iCalendar format (UTC)
  private formatICalDate(date: Date, isAllDay: boolean = false): string {
    if (isAllDay) {
      return date.toISOString().split('T')[0].replace(/-/g, '');
    }
    return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
  }

  // Parse iCalendar date string and convert to UTC+7 string
  private parseICalDate(icalDate: string, isAllDay: boolean = false): string {
    if (isAllDay) {
      const year = icalDate.slice(0, 4);
      const month = icalDate.slice(4, 6);
      const day = icalDate.slice(6, 8);
      // All-day events don't need timezone conversion
      return `${year}-${month}-${day}`;
    }
    // Parse YYYYMMDDTHHMMSSZ format (UTC)
    const year = icalDate.slice(0, 4);
    const month = icalDate.slice(4, 6);
    const day = icalDate.slice(6, 8);
    const hour = icalDate.slice(9, 11);
    const minute = icalDate.slice(11, 13);
    const second = icalDate.slice(13, 15);
    
    // Parse as UTC, then add 7 hours to get UTC+7
    const utcDate = new Date(`${year}-${month}-${day}T${hour}:${minute}:${second}Z`);
    const utc7Date = new Date(utcDate.getTime() + (7 * 60 * 60 * 1000));
    
    // Format as ISO string with UTC+7 timezone
    return utc7Date.toISOString().replace('Z', '+07:00');
  }

  // Parse ISO 8601 duration to minutes
  private parseDurationToMinutes(duration: string): number {
    // Handle negative triggers (before event)
    const isNegative = duration.startsWith('-');
    const cleanDuration = duration.replace(/^-/, '');
    
    let minutes = 0;
    
    // Parse P[n]D format (days)
    const dayMatch = cleanDuration.match(/P(\d+)D/);
    if (dayMatch) {
      minutes += parseInt(dayMatch[1]) * 24 * 60;
    }
    
    // Parse PT[n]H[n]M format (hours/minutes)
    const hourMatch = cleanDuration.match(/(\d+)H/);
    if (hourMatch) {
      minutes += parseInt(hourMatch[1]) * 60;
    }
    
    const minMatch = cleanDuration.match(/(\d+)M/);
    if (minMatch) {
      minutes += parseInt(minMatch[1]);
    }
    
    return isNegative ? minutes : -minutes; // Negative duration = before event
  }

  // Convert CreateReminderOptions to trigger string
  private buildTrigger(options: CreateReminderOptions): string {
    let totalMinutes = 0;
    
    if (options.daysBefore) {
      totalMinutes += options.daysBefore * 24 * 60;
    }
    if (options.hoursBefore) {
      totalMinutes += options.hoursBefore * 60;
    }
    if (options.minutesBefore) {
      totalMinutes += options.minutesBefore;
    }
    
    // Default to 15 minutes if nothing specified
    if (totalMinutes === 0) {
      totalMinutes = 15;
    }
    
    // Build ISO 8601 duration
    const days = Math.floor(totalMinutes / (24 * 60));
    const hours = Math.floor((totalMinutes % (24 * 60)) / 60);
    const minutes = totalMinutes % 60;
    
    let trigger = '-P';
    if (days > 0) {
      trigger += `${days}D`;
    }
    if (hours > 0 || minutes > 0) {
      trigger += 'T';
      if (hours > 0) trigger += `${hours}H`;
      if (minutes > 0) trigger += `${minutes}M`;
    }
    
    return trigger;
  }

  // Build VALARM string
  private buildVAlarm(reminder: CreateReminderOptions, reminderId: string): string {
    const trigger = this.buildTrigger(reminder);
    const action = (reminder.action || 'display').toUpperCase();
    const description = reminder.description || 'Event reminder';
    
    return `BEGIN:VALARM
ACTION:${action}
TRIGGER:${trigger}
DESCRIPTION:${description}
X-WR-ALARMUID:${reminderId}
END:VALARM`;
  }

  // Parse VALARM from ICS data
  private parseVAlarms(icsData: string): Reminder[] {
    const reminders: Reminder[] = [];
    const alarmRegex = /BEGIN:VALARM[\s\S]*?END:VALARM/g;
    const alarms = icsData.match(alarmRegex) || [];
    
    for (const alarm of alarms) {
      const lines = alarm.split('\n');
      let reminder: Partial<Reminder> = {};
      
      for (const line of lines) {
        const trimmed = line.trim();
        
        if (trimmed.startsWith('TRIGGER:')) {
          reminder.trigger = trimmed.slice(8);
          reminder.minutesBefore = this.parseDurationToMinutes(reminder.trigger);
        } else if (trimmed.startsWith('ACTION:')) {
          reminder.action = trimmed.slice(7).toLowerCase() as 'display' | 'audio' | 'email';
        } else if (trimmed.startsWith('DESCRIPTION:')) {
          reminder.description = trimmed.slice(12);
        } else if (trimmed.startsWith('X-WR-ALARMUID:')) {
          reminder.id = trimmed.slice(14);
        }
      }
      
      // Generate ID if not found
      if (!reminder.id) {
        reminder.id = uuidv4();
      }
      
      if (reminder.trigger) {
        reminders.push(reminder as Reminder);
      }
    }
    
    return reminders;
  }

  // Extract event data from iCalendar string
  private parseEventData(icsData: string, calendarId: string, url: string, etag: string): CalendarEvent {
    const lines = icsData.split('\n');
    let event: Partial<CalendarEvent> = { calendarId, url, etag };
    let inEvent = false;
    let isAllDay = false;

    for (const line of lines) {
      const trimmed = line.trim();
      
      if (trimmed === 'BEGIN:VEVENT') {
        inEvent = true;
        continue;
      }
      if (trimmed === 'END:VEVENT') {
        break;
      }
      if (!inEvent) continue;

      if (trimmed.startsWith('UID:')) {
        event.id = trimmed.slice(4);
      } else if (trimmed.startsWith('SUMMARY:')) {
        event.title = trimmed.slice(8);
      } else if (trimmed.startsWith('DESCRIPTION:')) {
        event.description = trimmed.slice(12);
      } else if (trimmed.startsWith('LOCATION:')) {
        event.location = trimmed.slice(9);
      } else if (trimmed.startsWith('DTSTART;VALUE=DATE:')) {
        isAllDay = true;
        const dateStr = trimmed.slice(19);
        event.start = this.parseICalDate(dateStr, true);
      } else if (trimmed.startsWith('DTSTART:')) {
        const dateStr = trimmed.slice(8);
        event.start = this.parseICalDate(dateStr, false);
      } else if (trimmed.startsWith('DTEND;VALUE=DATE:')) {
        const dateStr = trimmed.slice(17);
        event.end = this.parseICalDate(dateStr, true);
      } else if (trimmed.startsWith('DTEND:')) {
        const dateStr = trimmed.slice(6);
        event.end = this.parseICalDate(dateStr, false);
      } else if (trimmed.startsWith('RRULE:')) {
        event.recurrence = trimmed.slice(6);
      }
    }

    event.isAllDay = isAllDay;
    
    // Parse reminders/alarms
    event.reminders = this.parseVAlarms(icsData);
    
    return event as CalendarEvent;
  }

  // Build iCalendar string from event data
  private buildICalEvent(
    event: CreateEventOptions, 
    eventId: string, 
    recurrence?: string,
    reminders?: CreateReminderOptions[]
  ): string {
    const startUTC = this.toUTC(event.start);
    const endUTC = this.toUTC(event.end);
    const startDate = new Date(startUTC);
    const endDate = new Date(endUTC);

    let icsData = `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Fastmail MCP Server//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
UID:${eventId}
`;

    if (event.allDay) {
      icsData += `DTSTART;VALUE=DATE:${this.formatICalDate(startDate, true)}
DTEND;VALUE=DATE:${this.formatICalDate(endDate, true)}
`;
    } else {
      icsData += `DTSTART:${this.formatICalDate(startDate)}
DTEND:${this.formatICalDate(endDate)}
`;
    }

    icsData += `SUMMARY:${event.title}
`;

    if (event.description) {
      icsData += `DESCRIPTION:${event.description}\n`;
    }

    if (event.location) {
      icsData += `LOCATION:${event.location}\n`;
    }

    if (recurrence) {
      icsData += `RRULE:${recurrence}\n`;
    }

    if (event.attendees && event.attendees.length > 0) {
      for (const attendee of event.attendees) {
        const attendeeStr = attendee.name
          ? `CN="${attendee.name}":mailto:${attendee.email}`
          : `mailto:${attendee.email}`;
        icsData += `ATTENDEE;${attendeeStr}\n`;
      }
    }

    // Add reminders/alarms
    const alarmsToAdd = reminders || event.reminders || [];
    for (const reminder of alarmsToAdd) {
      const reminderId = uuidv4();
      icsData += this.buildVAlarm(reminder, reminderId) + '\n';
    }

    icsData += `STATUS:CONFIRMED
SEQUENCE:0
END:VEVENT
END:VCALENDAR`;

    return icsData;
  }

  async listCalendars(): Promise<Calendar[]> {
    const calendars = await this.client.getCalendars();
    
    return calendars.map(cal => ({
      id: cal.url,
      name: typeof cal.displayName === 'string' ? cal.displayName : 'Unnamed Calendar',
      description: cal.description,
      color: cal.calendarColor,
      timezone: cal.timezone,
    }));
  }

  async listEvents(
    calendarId?: string,
    startDate?: string,
    endDate?: string
  ): Promise<CalendarEvent[]> {
    const calendars = await this.client.getCalendars();
    let targetCalendars: DAVCalendar[];

    if (calendarId) {
      const cal = calendars.find(c => c.url === calendarId || c.displayName === calendarId);
      if (!cal) throw new Error(`Calendar not found: ${calendarId}`);
      targetCalendars = [cal];
    } else {
      targetCalendars = calendars;
    }

    // Normalize date range to cover full days
    let effectiveStartDate = startDate;
    let effectiveEndDate = endDate;

    if (startDate) {
      // If startDate has no time component (just YYYY-MM-DD), add start of day time
      if (!startDate.includes('T')) {
        effectiveStartDate = `${startDate}T00:00:00`;
      }
    }

    if (endDate) {
      // If endDate has no time component (just YYYY-MM-DD), add end of day time
      if (!endDate.includes('T')) {
        effectiveEndDate = `${endDate}T23:59:59`;
      }
    } else if (startDate && !endDate) {
      // If only startDate provided (single day query), set end to end of that day
      const datePart = startDate.split('T')[0];
      effectiveEndDate = `${datePart}T23:59:59`;
    }

    const timeRange = {
      start: effectiveStartDate ? this.toUTC(effectiveStartDate) : new Date().toISOString(),
      end: effectiveEndDate ? this.toUTC(effectiveEndDate) : new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
    };

    const allEvents: CalendarEvent[] = [];

    for (const calendar of targetCalendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar, timeRange);
        
        for (const obj of objects) {
          if (obj.data && obj.url && obj.etag) {
            const event = this.parseEventData(obj.data, calendar.url, obj.url, obj.etag);
            allEvents.push(event);
          }
        }
      } catch (error) {
        console.error(`Error fetching events from ${calendar.displayName}:`, error);
      }
    }

    // Sort by start date
    return allEvents.sort((a, b) => new Date(a.start).getTime() - new Date(b.start).getTime());
  }

  async getEvent(eventId: string): Promise<CalendarEvent> {
    const calendars = await this.client.getCalendars();
    
    for (const calendar of calendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar);
        
        for (const obj of objects) {
          if (obj.url?.includes(eventId) && obj.data && obj.etag) {
            return this.parseEventData(obj.data, calendar.url, obj.url, obj.etag);
          }
        }
      } catch (error) {
        console.error(`Error searching in ${calendar.displayName}:`, error);
      }
    }

    throw new Error(`Event not found: ${eventId}`);
  }

  async createEvent(
    calendarId: string | undefined,
    options: CreateEventOptions
  ): Promise<{ id: string }> {
    const calendars = await this.client.getCalendars();
    let calendar: DAVCalendar;

    if (calendarId) {
      const cal = calendars.find(c => c.url === calendarId || c.displayName === calendarId);
      if (!cal) throw new Error(`Calendar not found: ${calendarId}`);
      calendar = cal;
    } else {
      // Find a proper calendar (not a task calendar)
      calendar = calendars.find(c => 
        c.displayName && 
        !(c.displayName as string).toLowerCase().includes('task') &&
        !(c.displayName as string).toLowerCase().includes('default')
      ) || calendars[0];
      if (!calendar) throw new Error('No calendars found');
    }

    const eventId = uuidv4();
    const icsData = this.buildICalEvent(options, eventId);

    await this.client.createEvent(calendar, icsData, eventId);

    return { id: eventId };
  }

  async updateEvent(
    eventId: string,
    updates: Partial<CreateEventOptions>
  ): Promise<void> {
    const calendars = await this.client.getCalendars();
    
    for (const calendar of calendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar);
        
        for (const obj of objects) {
          if (obj.url?.includes(eventId) && obj.data && obj.etag) {
            // Parse existing event
            const existing = this.parseEventData(obj.data, calendar.url, obj.url, obj.etag);
            
            // Merge updates
            const updated: CreateEventOptions = {
              title: updates.title || existing.title,
              start: updates.start || existing.start,
              end: updates.end || existing.end,
              description: updates.description !== undefined ? updates.description : existing.description,
              location: updates.location !== undefined ? updates.location : existing.location,
              allDay: updates.allDay !== undefined ? updates.allDay : existing.isAllDay,
              attendees: updates.attendees || existing.attendees,
            };

            const icsData = this.buildICalEvent(updated, eventId, existing.recurrence);
            
            await this.client.updateEvent(calendar, obj, icsData);
            return;
          }
        }
      } catch (error) {
        console.error(`Error searching in ${calendar.displayName}:`, error);
      }
    }

    throw new Error(`Event not found: ${eventId}`);
  }

  async deleteEvent(eventId: string): Promise<void> {
    const calendars = await this.client.getCalendars();
    
    for (const calendar of calendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar);
        
        for (const obj of objects) {
          if (obj.url?.includes(eventId)) {
            await this.client.deleteEvent(obj);
            return;
          }
        }
      } catch (error) {
        console.error(`Error searching in ${calendar.displayName}:`, error);
      }
    }

    throw new Error(`Event not found: ${eventId}`);
  }

  async searchEvents(
    query: string,
    startDate?: string,
    endDate?: string
  ): Promise<CalendarEvent[]> {
    const events = await this.listEvents(undefined, startDate, endDate);
    const lowerQuery = query.toLowerCase();
    
    return events.filter(event => 
      event.title.toLowerCase().includes(lowerQuery) ||
      (event.description && event.description.toLowerCase().includes(lowerQuery)) ||
      (event.location && event.location.toLowerCase().includes(lowerQuery))
    );
  }

  async createRecurringEvent(
    calendarId: string | undefined,
    options: CreateRecurringEventOptions
  ): Promise<{ id: string }> {
    const calendars = await this.client.getCalendars();
    let calendar: DAVCalendar;

    if (calendarId) {
      const cal = calendars.find(c => c.url === calendarId || c.displayName === calendarId);
      if (!cal) throw new Error(`Calendar not found: ${calendarId}`);
      calendar = cal;
    } else {
      calendar = calendars[0];
      if (!calendar) throw new Error('No calendars found');
    }

    // Build RRULE
    let rrule = `FREQ=${options.recurrence.toUpperCase()}`;
    
    if (options.recurrenceCount) {
      rrule += `;COUNT=${options.recurrenceCount}`;
    } else if (options.recurrenceUntil) {
      // Convert to UTC for RRULE
      const untilUTC = this.toUTC(options.recurrenceUntil + 'T23:59:59');
      const untilDate = new Date(untilUTC);
      rrule += `;UNTIL=${this.formatICalDate(untilDate)}`;
    }

    const eventId = uuidv4();
    const icsData = this.buildICalEvent(options, eventId, rrule);

    await this.client.createEvent(calendar, icsData, eventId);

    return { id: eventId };
  }

  async addReminder(
    eventId: string,
    options: CreateReminderOptions
  ): Promise<{ id: string }> {
    const calendars = await this.client.getCalendars();
    
    for (const calendar of calendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar);
        
        for (const obj of objects) {
          if (obj.url?.includes(eventId) && obj.data && obj.etag) {
            // Parse existing event
            const existing = this.parseEventData(obj.data, calendar.url, obj.url, obj.etag);
            
            // Add new reminder
            const existingReminders = existing.reminders?.map(r => ({
              minutesBefore: r.minutesBefore,
              action: r.action,
              description: r.description,
            })) || [];
            
            const allReminders = [...existingReminders, options];
            
            // Rebuild event with reminders
            const updated: CreateEventOptions = {
              title: existing.title,
              start: existing.start,
              end: existing.end,
              description: existing.description,
              location: existing.location,
              allDay: existing.isAllDay,
              attendees: existing.attendees,
            };

            const icsData = this.buildICalEvent(updated, eventId, existing.recurrence, allReminders);
            
            await this.client.updateEvent(calendar, obj, icsData);
            
            const newReminderId = uuidv4();
            return { id: newReminderId };
          }
        }
      } catch (error) {
        console.error(`Error searching in ${calendar.displayName}:`, error);
      }
    }

    throw new Error(`Event not found: ${eventId}`);
  }

  async removeReminder(eventId: string, reminderId?: string): Promise<void> {
    const calendars = await this.client.getCalendars();
    
    for (const calendar of calendars) {
      try {
        const objects = await this.client.fetchCalendarObjects(calendar);
        
        for (const obj of objects) {
          if (obj.url?.includes(eventId) && obj.data && obj.etag) {
            // Parse existing event
            const existing = this.parseEventData(obj.data, calendar.url, obj.url, obj.etag);
            
            // Filter out the reminder
            let remainingReminders: CreateReminderOptions[] = [];
            
            if (reminderId && existing.reminders) {
              remainingReminders = existing.reminders
                .filter(r => r.id !== reminderId)
                .map(r => ({
                  minutesBefore: r.minutesBefore,
                  action: r.action,
                  description: r.description,
                }));
            }
            // If no reminderId, remove all reminders (remainingReminders stays empty)
            
            // Rebuild event
            const updated: CreateEventOptions = {
              title: existing.title,
              start: existing.start,
              end: existing.end,
              description: existing.description,
              location: existing.location,
              allDay: existing.isAllDay,
              attendees: existing.attendees,
            };

            const icsData = this.buildICalEvent(updated, eventId, existing.recurrence, remainingReminders);
            
            await this.client.updateEvent(calendar, obj, icsData);
            return;
          }
        }
      } catch (error) {
        console.error(`Error searching in ${calendar.displayName}:`, error);
      }
    }

    throw new Error(`Event not found: ${eventId}`);
  }

  async listReminders(eventId: string): Promise<Reminder[]> {
    const event = await this.getEvent(eventId);
    return event.reminders || [];
  }
}
