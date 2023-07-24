import org.apache.fineract.commands.service.CommandWrapper;
import org.apache.fineract.infrastructure.core.api.JsonCommand;
import org.apache.fineract.infrastructure.core.data.CommandProcessingResult;
import org.apache.fineract.infrastructure.core.serialization.FromJsonHelper;
import org.apache.fineract.infrastructure.core.service.RoutingDataSource;
import org.apache.fineract.portfolio.account.api.AccountTransfersApiResource;
import org.apache.fineract.useradministration.domain.AppUser;
import org.junit.Before;
import org.junit.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.mockito.Mockito.*;

public class AccountTransfersApiResourceTest {

    @InjectMocks
    private AccountTransfersApiResource accountTransfersApiResource;

    @Mock
    private FromJsonHelper fromApiJsonDeserializer;

    @Mock
    private RoutingDataSource dataSource;

    @Before
    public void setup() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testCreateTransferSuccess() {
        String apiRequestBodyAsJson = "apiRequestBodyAsJson";
        when(fromApiJsonDeserializer.validateForCreate(anyString())).thenReturn(null);
        String result = accountTransfersApiResource.create(apiRequestBodyAsJson);
        verify(fromApiJsonDeserializer, times(1)).validateForCreate(anyString());
    }

    @Test
    public void testCreateTransferFailure() {
        String apiRequestBodyAsJson = "apiRequestBodyAsJson";
        when(fromApiJsonDeserializer.validateForCreate(anyString())).thenThrow(new RuntimeException());
        String result = accountTransfersApiResource.create(apiRequestBodyAsJson);
        verify(fromApiJsonDeserializer, times(1)).validateForCreate(anyString());
    }

    @Test
    public void testCreateTransferWithDifferentInput() {
        String apiRequestBodyAsJson = "differentApiRequestBodyAsJson";
        when(fromApiJsonDeserializer.validateForCreate(anyString())).thenReturn(null);
        String result = accountTransfersApiResource.create(apiRequestBodyAsJson);
        verify(fromApiJsonDeserializer, times(1)).validateForCreate(anyString());
    }
}