import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.junit.jupiter.api.Assertions.*;
import org.apache.fineract.portfolio.calendar.service.CalendarUtils;
import net.fortuna.ical4j.model.Recur;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Date;

@ExtendWith(MockitoExtension.class)
public class CalendarUtilsTest {

    @InjectMocks
    private CalendarUtils calendarUtils;

    @Mock
    private Recur recur;

    @Test
    public void testGetNextRecurringDateWithLocalDate() {
        LocalDate seedDate = LocalDate.now();
        LocalDate startDate = LocalDate.now().plusDays(1);
        Mockito.when(recur.getNextDate(Mockito.any(), Mockito.any())).thenReturn(new Date());
        LocalDate result = calendarUtils.getNextRecurringDate(recur, seedDate, startDate);
        assertNotNull(result);
    }

    @Test
    public void testGetNextRecurringDateWithLocalDateTime() {
        LocalDateTime seedDate = LocalDateTime.now();
        LocalDateTime startDate = LocalDateTime.now().plusDays(1);
        Mockito.when(recur.getNextDate(Mockito.any(), Mockito.any())).thenReturn(new Date());
        LocalDateTime result = calendarUtils.getNextRecurringDate(recur, seedDate, startDate);
        assertNotNull(result);
    }

    @Test
    public void testGetNextRecurringDateWithRecurringRule() {
        String recurringRule = "FREQ=DAILY;INTERVAL=1";
        LocalDateTime seedDate = LocalDateTime.now();
        LocalDateTime startDate = LocalDateTime.now().plusDays(1);
        LocalDateTime result = calendarUtils.getNextRecurringDate(recurringRule, seedDate, startDate);
        assertNotNull(result);
    }
}
