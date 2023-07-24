import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.junit.jupiter.api.Assertions.*;
import org.apache.fineract.portfolio.savings.DepositAccountOnClosureType;

@ExtendWith(MockitoExtension.class)
public class DepositAccountOnClosureTypeTest {

    @InjectMocks
    private DepositAccountOnClosureType depositAccountOnClosureType;

    @Test
    public void testFromIntWithValidValue() {
        Integer closureTypeValue = 100;
        DepositAccountOnClosureType result = DepositAccountOnClosureType.fromInt(closureTypeValue);
        assertEquals(DepositAccountOnClosureType.WITHDRAW_DEPOSIT, result);
    }

    @Test
    public void testFromIntWithInvalidValue() {
        Integer closureTypeValue = 500;
        DepositAccountOnClosureType result = DepositAccountOnClosureType.fromInt(closureTypeValue);
        assertEquals(DepositAccountOnClosureType.INVALID, result);
    }

    @Test
    public void testFromIntWithNullValue() {
        Integer closureTypeValue = null;
        DepositAccountOnClosureType result = DepositAccountOnClosureType.fromInt(closureTypeValue);
        assertEquals(DepositAccountOnClosureType.INVALID, result);
    }
}
