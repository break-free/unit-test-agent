import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.junit.jupiter.api.Assertions.*;
import org.apache.fineract.useradministration.service.UserDataValidator;
import org.apache.fineract.infrastructure.core.serialization.FromJsonHelper;
import org.apache.fineract.useradministration.domain.PasswordValidationPolicyRepository;
import com.google.gson.JsonElement;

@ExtendWith(MockitoExtension.class)
public class UserDataValidatorTest {

    @InjectMocks
    private UserDataValidator userDataValidator;

    @Mock
    private FromJsonHelper fromApiJsonHelper;

    @Mock
    private PasswordValidationPolicyRepository passwordValidationPolicy;

    @Mock
    private JsonElement jsonElement;

    @Test
    public void testValidateForCreateWithValidJson() {
        String json = "{\"username\":\"testUser\",\"firstname\":\"test\",\"lastname\":\"user\",\"sendPasswordToEmail\":true,\"email\":\"testuser@test.com\",\"officeId\":1,\"roles\":[\"admin\"]}";
        Mockito.when(fromApiJsonHelper.parse(json)).thenReturn(jsonElement);
        Mockito.when(fromApiJsonHelper.extractStringNamed(Mockito.anyString(), Mockito.any())).thenReturn("test");
        Mockito.when(fromApiJsonHelper.extractBooleanNamed(Mockito.anyString(), Mockito.any())).thenReturn(true);
        Mockito.when(fromApiJsonHelper.extractLongNamed(Mockito.anyString(), Mockito.any())).thenReturn(1L);
        assertDoesNotThrow(() -> userDataValidator.validateForCreate(json));
    }

    @Test
    public void testValidateForCreateWithInvalidJson() {
        String json = "{\"username\":\"\",\"firstname\":\"\",\"lastname\":\"\",\"sendPasswordToEmail\":true,\"email\":\"\",\"officeId\":-1,\"roles\":[]}";
        Mockito.when(fromApiJsonHelper.parse(json)).thenReturn(jsonElement);
        Mockito.when(fromApiJsonHelper.extractStringNamed(Mockito.anyString(), Mockito.any())).thenReturn("");
        Mockito.when(fromApiJsonHelper.extractBooleanNamed(Mockito.anyString(), Mockito.any())).thenReturn(true);
        Mockito.when(fromApiJsonHelper.extractLongNamed(Mockito.anyString(), Mockito.any())).thenReturn(-1L);
        assertThrows(InvalidJsonException.class, () -> userDataValidator.validateForCreate(json));
    }

    @Test
    public void testValidateForCreateWithNullJson() {
        String json = null;
        assertThrows(InvalidJsonException.class, () -> userDataValidator.validateForCreate(json));
    }
}
