import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.InjectMocks;
import org.mockito.MockitoAnnotations;
import org.apache.fineract.portfolio.savings.DepositAccountUtils;
import org.apache.fineract.infrastructure.core.domain.PeriodFrequencyType;
import org.joda.time.LocalDate;

public class DepositAccountUtilsTest {

    @InjectMocks
    DepositAccountUtils depositAccountUtils;

    @BeforeEach
    public void init() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testCalculateNextDepositDate_WhenFrequencyIsDays() {
        LocalDate lastDepositDate = LocalDate.now();
        PeriodFrequencyType frequency = PeriodFrequencyType.DAYS;
        int recurringEvery = 5;
        LocalDate result = DepositAccountUtils.calculateNextDepositDate(lastDepositDate, frequency, recurringEvery);
        assert(result.equals(lastDepositDate.plusDays(recurringEvery)));
    }

    @Test
    public void testCalculateNextDepositDate_WhenFrequencyIsMonths() {
        LocalDate lastDepositDate = LocalDate.now();
        PeriodFrequencyType frequency = PeriodFrequencyType.MONTHS;
        int recurringEvery = 2;
        LocalDate result = DepositAccountUtils.calculateNextDepositDate(lastDepositDate, frequency, recurringEvery);
        assert(result.equals(lastDepositDate.plusMonths(recurringEvery)));
    }

    @Test
    public void testCalculateNextDepositDate_WhenFrequencyIsInvalid() {
        LocalDate lastDepositDate = LocalDate.now();
        PeriodFrequencyType frequency = PeriodFrequencyType.INVALID;
        int recurringEvery = 2;
        LocalDate result = DepositAccountUtils.calculateNextDepositDate(lastDepositDate, frequency, recurringEvery);
        assert(result.equals(lastDepositDate));
    }
}
