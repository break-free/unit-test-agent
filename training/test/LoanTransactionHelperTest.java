import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

import org.apache.fineract.integrationtests.common.loans.LoanTransactionHelper;
import io.restassured.specification.RequestSpecification;
import io.restassured.specification.ResponseSpecification;
import java.util.ArrayList;
import java.util.HashMap;

public class LoanTransactionHelperTest {

    @Mock
    private RequestSpecification requestSpec;

    @Mock
    private ResponseSpecification responseSpec;

    @InjectMocks
    private LoanTransactionHelper loanTransactionHelper;

    @BeforeEach
    public void setup() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testGetLoanFutureRepaymentSchedule() {
        Integer loanID = 1;
        HashMap<String, Object> response = new HashMap<>();
        ArrayList<Object> futurePeriods = new ArrayList<>();
        response.put("futurePeriods", futurePeriods);

        when(requestSpec.get(anyString())).thenReturn(response);

        ArrayList result = loanTransactionHelper.getLoanFutureRepaymentSchedule(requestSpec, responseSpec, loanID);
        assertEquals(futurePeriods, result);
    }

    @Test
    public void testGetLoanFutureRepaymentScheduleWithNoFuturePeriods() {
        Integer loanID = 1;
        HashMap<String, Object> response = new HashMap<>();

        when(requestSpec.get(anyString())).thenReturn(response);

        ArrayList result = loanTransactionHelper.getLoanFutureRepaymentSchedule(requestSpec, responseSpec, loanID);
        assertNull(result);
    }

    @Test
    public void testGetLoanFutureRepaymentScheduleWithInvalidLoanID() {
        Integer loanID = -1;
        HashMap<String, Object> response = new HashMap<>();
        ArrayList<Object> futurePeriods = new ArrayList<>();
        response.put("futurePeriods", futurePeriods);

        when(requestSpec.get(anyString())).thenReturn(response);

        ArrayList result = loanTransactionHelper.getLoanFutureRepaymentSchedule(requestSpec, responseSpec, loanID);
        assertEquals(futurePeriods, result);
    }
}
