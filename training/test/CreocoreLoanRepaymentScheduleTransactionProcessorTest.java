import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.apache.fineract.portfolio.loanaccount.domain.transactionprocessor.impl.CreocoreLoanRepaymentScheduleTransactionProcessor;
import org.apache.fineract.portfolio.loanaccount.domain.LoanTransaction;
import org.apache.fineract.portfolio.loanaccount.domain.transactionprocessor.impl.LoanRepaymentScheduleInstallment;
import org.apache.fineract.portfolio.loanaccount.domain.transactionprocessor.impl.LoanTransactionToRepaymentScheduleMapping;
import org.apache.fineract.organisation.monetary.domain.MonetaryCurrency;
import org.apache.fineract.organisation.monetary.domain.Money;
import org.joda.time.LocalDate;

import java.util.List;
import java.util.ArrayList;

import static org.mockito.Mockito.*;

public class CreocoreLoanRepaymentScheduleTransactionProcessorTest {

    @InjectMocks
    CreocoreLoanRepaymentScheduleTransactionProcessor processor;

    @Mock
    LoanRepaymentScheduleInstallment currentInstallment;

    @Mock
    LoanTransaction loanTransaction;

    @Mock
    Money transactionAmountUnprocessed;

    @Mock
    List<LoanTransactionToRepaymentScheduleMapping> transactionMappings;

    @BeforeEach
    public void init() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testHandleTransactionThatIsOnTimePaymentOfInstallment_WhenTransactionIsChargesWaiver() {
        when(loanTransaction.isChargesWaiver()).thenReturn(true);
        processor.handleTransactionThatIsOnTimePaymentOfInstallment(currentInstallment, loanTransaction, transactionAmountUnprocessed, transactionMappings);
        verify(currentInstallment, times(0)).waiveInterestComponent(any(), any());
    }

    @Test
    public void testHandleTransactionThatIsOnTimePaymentOfInstallment_WhenTransactionIsInterestWaiver() {
        when(loanTransaction.isInterestWaiver()).thenReturn(true);
        processor.handleTransactionThatIsOnTimePaymentOfInstallment(currentInstallment, loanTransaction, transactionAmountUnprocessed, transactionMappings);
        verify(currentInstallment, times(1)).waiveInterestComponent(any(), any());
    }

    @Test
    public void testHandleTransactionThatIsOnTimePaymentOfInstallment_WhenTransactionIsChargePayment() {
        when(loanTransaction.isChargePayment()).thenReturn(true);
        processor.handleTransactionThatIsOnTimePaymentOfInstallment(currentInstallment, loanTransaction, transactionAmountUnprocessed, transactionMappings);
        verify(currentInstallment, times(1)).payFeeChargesComponent(any(), any());
    }
}
