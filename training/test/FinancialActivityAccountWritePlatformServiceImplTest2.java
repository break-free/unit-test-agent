mport org.apache.fineract.accounting.financialactivityaccount.service.FinancialActivityAccountWritePlatformServiceImpl;
import org.apache.fineract.commands.domain.Command;
import org.apache.fineract.commands.service.CommandWrapper;
import org.apache.fineract.infrastructure.core.api.JsonCommand;
import org.apache.fineract.infrastructure.core.data.CommandProcessingResult;
import org.apache.fineract.infrastructure.core.serialization.FromJsonHelper;
import org.apache.fineract.infrastructure.core.service.RoutingDataSource;
import org.apache.fineract.useradministration.domain.AppUser;
import org.junit.Before;
import org.junit.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.mockito.Mockito.*;

public class FinancialActivityAccountWritePlatformServiceImplTest2 {

    @InjectMocks
    private FinancialActivityAccountWritePlatformServiceImpl financialActivityAccountWritePlatformService;

    @Mock
    private FromJsonHelper fromApiJsonDeserializer;

    @Mock
    private RoutingDataSource dataSource;

    @Before
    public void setup() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testUpdateGLAccountActivityMappingSuccess() {
        Long financialActivityAccountId = 1L;
        JsonCommand command = mock(JsonCommand.class);
        when(fromApiJsonDeserializer.validateForUpdate(anyString())).thenReturn(null);
        CommandProcessingResult result = financialActivityAccountWritePlatformService.updateGLAccountActivityMapping(financialActivityAccountId, command);
        verify(fromApiJsonDeserializer, times(1)).validateForUpdate(anyString());
    }

    @Test
    public void testUpdateGLAccountActivityMappingFailure() {
        Long financialActivityAccountId = 1L;
        JsonCommand command = mock(JsonCommand.class);
        when(fromApiJsonDeserializer.validateForUpdate(anyString())).thenThrow(new RuntimeException());
        CommandProcessingResult result = financialActivityAccountWritePlatformService.updateGLAccountActivityMapping(financialActivityAccountId, command);
        verify(fromApiJsonDeserializer, times(1)).validateForUpdate(anyString());
    }

    @Test
    public void testUpdateGLAccountActivityMappingWithChanges() {
        Long financialActivityAccountId = 1L;
        JsonCommand command = mock(JsonCommand.class);
        when(fromApiJsonDeserializer.validateForUpdate(anyString())).thenReturn(null);
        when(command.mapValueOfParameterNamed(anyString())).thenReturn(new HashMap<>());
        CommandProcessingResult result = financialActivityAccountWritePlatformService.updateGLAccountActivityMapping(financialActivityAccountId, command);
        verify(fromApiJsonDeserializer, times(1)).validateForUpdate(anyString());
    }
}
