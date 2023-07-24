import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.junit.jupiter.api.Assertions.*;
import org.apache.fineract.portfolio.paymentdetail.service.PaymentDetailWritePlatformServiceJpaRepositoryImpl;
import org.apache.fineract.portfolio.paymentdetail.domain.PaymentDetail;
import org.apache.fineract.portfolio.paymentdetail.domain.PaymentType;
import org.apache.fineract.infrastructure.core.api.JsonCommand;
import java.util.Map;
import java.util.HashMap;

@ExtendWith(MockitoExtension.class)
public class PaymentDetailWritePlatformServiceJpaRepositoryImplTest {

    @InjectMocks
    private PaymentDetailWritePlatformServiceJpaRepositoryImpl paymentDetailWritePlatformService;

    @Mock
    private JsonCommand command;

    @Mock
    private PaymentType paymentType;

    @Mock
    private PaymentDetail paymentDetail;

    @Test
    public void testCreatePaymentDetailWithValidPaymentTypeId() {
        Long paymentTypeId = 1L;
        Mockito.when(command.longValueOfParameterNamed(Mockito.anyString())).thenReturn(paymentTypeId);
        Mockito.when(paymentDetailWritePlatformService.createPaymentDetail(command, new HashMap<>())).thenReturn(paymentDetail);
        PaymentDetail result = paymentDetailWritePlatformService.createPaymentDetail(command, new HashMap<>());
        assertNotNull(result);
    }

    @Test
    public void testCreatePaymentDetailWithInvalidPaymentTypeId() {
        Long paymentTypeId = -1L;
        Mockito.when(command.longValueOfParameterNamed(Mockito.anyString())).thenReturn(paymentTypeId);
        Mockito.when(paymentDetailWritePlatformService.createPaymentDetail(command, new HashMap<>())).thenReturn(null);
        PaymentDetail result = paymentDetailWritePlatformService.createPaymentDetail(command, new HashMap<>());
        assertNull(result);
    }

    @Test
    public void testCreatePaymentDetailWithNullPaymentTypeId() {
        Mockito.when(command.longValueOfParameterNamed(Mockito.anyString())).thenReturn(null);
        Mockito.when(paymentDetailWritePlatformService.createPaymentDetail(command, new HashMap<>())).thenReturn(null);
        PaymentDetail result = paymentDetailWritePlatformService.createPaymentDetail(command, new HashMap<>());
        assertNull(result);
    }
}
